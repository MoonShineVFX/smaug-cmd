from typing import List
from smaug_cmd.domain.smaug_types import AssetTemplate, MdJson
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain.operators import CategoryOp, MenuOp


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
    last_category = None
    for category in md_json["categories"]:
        parent_id = None
        if category["parent"] is not None:
            # 找出 parent_id
            parent_cates = CategoryOp.getByName(category["parent"])
            if parent_cates:
                parent_id = parent_cates[0]["id"]
        last_category = CategoryOp.create(
            category["cate_name"], parent_id, resources_menu_id
        )

    # 從assets 建立 asset_template 陣列
    asset_templates: List[AssetTemplate] = []
    for assets in md_json["assets"]:
        # 依照 md_json 的 assets 建立資產
        for idx, asset in enumerate(assets["data"]):
            asset_template = AssetTemplate(
                name=asset["asset_name"] + " " + str(idx),
                description=asset["description"],
                folder=asset["folder"],
                preview=asset["preview"],
                categoryId=last_category["id"],
            )
            asset_templates.append(asset_template)

    # 依照 md_json 的 assets 建立資產
