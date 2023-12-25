
import os
from typing import Generator, List, Dict
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain.operators import CategoryOp, MenuOp
from smaug_cmd.model.auth import log_in, log_out
from smaug_cmd.domain.exceptions import SmaugError

def smaug_resource_uploader(folder: str):
    """Upload a asset from resource team to smaug.

    :param base_dir: The base directory of the resource.
    :return: The resource id.
    """    
    # 從所有的 md 檔組合出分類結構
    for mb_file in _find_md_files(folder):
        md_json = ps.md_parsing(mb_file)
        md_uploader(md_json)

#     # 祭 resource menu 的 id
#     menus = MenuOp.all()

#     resources_menu_id = None
#     for menu in menus:
#         if menu["name"] == "Resources":
#             resources_menu_id = menu["id"]
#             break

#     if resources_menu_id is None:
#         raise SmaugError("Can't find Resources menu.")

#     # 依序建立分類
    
#     uploader_id = os.environ.get("UPLOADER_ID", "")
#     uploader_pw = os.environ.get("UPLOADER_PW", "")
#     log_in(uploader_id, uploader_pw)
#     for category in all_categories:
#         parent_id = None
#         if category['parent'] is not None:
#             # 找出 parent_id
#             parent_cates = CategoryOp.getByName(category['parent'])
#             if parent_cates:
#                 parent_id = parent_cates[0]['id']
#         CategoryOp.create(category["cate_name"], parent_id, resources_menu_id)
#     log_out()

def _find_md_files(md_file_folder) -> Generator[str, None, None]:
    for root, _, files in os.walk(md_file_folder):
        for file in files:
            if file.endswith(".md"):
                md_file = os.path.join(root, file)
                yield md_file


# def _md_upload(md_file):
#     md_json = ps.md_parsing(md_file)
#     md_uploader = ps.md_uploader(md_json)
#     md_uploader.upload()


if __name__=='__main__':
    smaug_resource_uploader(f"{os.environ.get('TEST_DATA_RESOURCE')}\\_Obsidian\\MoonShineAsset")