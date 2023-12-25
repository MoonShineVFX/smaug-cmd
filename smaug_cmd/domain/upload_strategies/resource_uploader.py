import os
from typing import Optional
from smaug_cmd.services.auth import log_in
from smaug_cmd.domain.smaug_types import CategoryCreateResponse, MdJson, MdAsset
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain.operators import CategoryOp, MenuOp
from smaug_cmd.domain.folder_class import FolderClassFactory 


def md_uploader(md_json: MdJson):
    # 找出 resource menu 的 id
    menus = MenuOp.all()
    resources_menu_id = None
    for menu in menus:
        if menu["name"] == "Resources":
            resources_menu_id = menu["id"]
            break
    if resources_menu_id is None:
        raise SmaugError("Can't find Resources menu.")

    # 依照 md_json 的 categories 建立分類，並保留最後一個建立的分類
    uploader_id = os.environ.get("UPLOADER_ID", "")
    uploader_pw = os.environ.get("UPLOADER_PW", "")
    user = log_in(uploader_id, uploader_pw)
    last_category = None
    for category in md_json["categories"]:
        # 確定是不是已有分類
        created = False
        cates = CategoryOp.getByNameAndParent(category["cate_name"], category["parent"], resources_menu_id)
        if cates:
            last_category = cates[0]
            created = True

        # 沒現存的就建一個
        if not created:
            parent_id = None
            if category["parent"] is not None:
                # 找出 parent_id
                parent_cates = CategoryOp.getByName(category["parent"])
                if parent_cates:
                    parent_id = parent_cates[0]["id"]
            last_category = CategoryOp.create(
                category["cate_name"], parent_id, resources_menu_id
        )
    if last_category is None:
        raise SmaugError("Can't find last category.")

    # 依照 md_json 的 assets 建立資產
    for md_assets in  md_json["assets"]:
        if (md_assets["data"]) == 1:
            for md_asset in md_assets["data"]:
                md_asset_uploader(md_asset, None, last_category, user["id"])
        else:
            for idx, md_asset in enumerate(md_assets["data"]):
                md_asset_uploader(md_asset, idx, last_category, user["id"])


def md_asset_uploader(md_asset: MdAsset, idx: Optional[int], category: CategoryCreateResponse, user_id: str):
    folder_obj = FolderClassFactory(md_asset["folder"]).create()
    if folder_obj is None:
        raise SmaugError(f"Can't find folder class for {md_asset['folder']}")

    asset_template = folder_obj.asset_template()
    asset_template["categoryId"] = category["id"]
    if idx is not None:
        asset_template["name"] = f"{asset_template['name']} {idx}"
    
    if md_asset["previews"]:
        asset_template["previews"] = md_asset["previews"]
    
    if md_asset["folder"]:
        asset_template["basedir"] = md_asset["folder"]
    
    # 看要不要拿 descript 去當 asset 的 tag

    if user_id is None:
        raise SmaugError("Can't get current user.")

    folder_obj.upload_asset(asset_template, user_id)
