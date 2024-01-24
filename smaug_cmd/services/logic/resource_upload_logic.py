import logging
from typing import Optional
from smaug_cmd.services.auth import current_user
from smaug_cmd.domain.smaug_types import CategoryCreateResponse, MdJson, MdAsset
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain.operators import CategoryOp, MenuOp
from smaug_cmd.domain.folder_class import FolderClassFactory 


logger = logging.getLogger("smaug_cmd.domain.resource_upload")


def md_uploader(md_json: MdJson):
    # 找出 resource menu 的 id
    menus = MenuOp.all()

    # Yung add
    # from smaug_cmd.domain.operators import CategoryOp, MenuOp
    logger.debug ( 'menus: %s', menus)
    
    resources_menu_id = None
    for menu in menus:
        if menu["name"] == "Resources":
            resources_menu_id = menu["id"]
            break
    if resources_menu_id is None:
        raise SmaugError("Can't find Resources menu.")

    # 依照 md_json 的 categories 建立分類，並保留最後一個建立的分類
    user = current_user()


    last_category = None
    for category in md_json["categories"]:
        # 確定是不是已有分類
        created = False
        cates = CategoryOp.getByNameAndParent(category["cate_name"], category["parent"], resources_menu_id)
        # from smaug_cmd.domain.operators import CategoryOp, MenuOp
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
    logger.info("%s is Created.", last_category['name'])

    # 依照 md_json 的 assets 建立資產
    for md_assets in  md_json["assets"]:
        logger.info("Uploading column %s", md_assets["kanbon_name"])
        md_assets_list = md_assets["data"]
        for idx, md_asset in enumerate(md_assets_list):
            
            # Yung add
            logger.debug( '>>>> idx: %s', idx )
            logger.debug( '>>>> md_asset: %s', md_asset )
            logger.debug( '>>>> last_category: %s', last_category )
            logger.debug( '>>>> user["id"]: %s\n', user["id"] )
            try:
                md_asset_uploader(md_asset, None, last_category, user["id"])

                # yung add
                # print ( "\n" ) 

            except SmaugError as e:
                logger.warning("Failed to upload asset. Reason: %s", e)

def md_asset_uploader(md_asset: MdAsset, idx: Optional[int], category: CategoryCreateResponse, user_id: str):
    factory = FolderClassFactory(md_asset["folder"])
    # from smaug_cmd.domain.folder_class import FolderClassFactory 
    # EX : "R:/_Asset/Game_Unreal/AncientEast/AsianTemple/"

    folder_obj = factory.create()

    # Yung add
    # print ( 'folder_obj: ', folder_obj )

    if folder_obj is None:
        raise SmaugError(f"Can't find folder class for {md_asset['folder']}")

    asset_template = folder_obj.asset_template()
    asset_template["categoryId"] = category["id"]
    if idx is not None:
        asset_template["name"] = f"{asset_template['name']} {idx}"
    
    # 用 md_asset 的資料覆蓋 asset_template
    if md_asset["previews"]:
        asset_template["previews"] = md_asset["previews"]
    
    if md_asset["folder"]:
        asset_template["basedir"] = md_asset["folder"]

    # Yung add
    # print ( 'asset_template: ', asset_template )
    
    # todo: 看要不要拿 description 去當 asset 的 tag

    if user_id is None:
        raise SmaugError("Can't get current user.")

    folder_obj.upload_asset(asset_template, user_id)

if __name__=='__main__':
    # print ( "Check" )
    # md_json = r'E:\Repos\smaug-cmd\test_Yung\Unreal_AncientEast 古代東方場景.json'
    # md_uploader(md_json)

    folder = "R:/_Asset/Game_Unreal/AncientEast/AsianTemple/"
    factory = FolderClassFactory(folder)
    folder_obj = factory.create()
    print ( 'folder_obj: ', folder_obj )
