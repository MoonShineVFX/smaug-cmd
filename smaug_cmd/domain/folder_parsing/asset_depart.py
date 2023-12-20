from pathlib import PureWindowsPath
from smaug_cmd.domain.folder_parsing import BaseFolder, util
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.setting import preview_factors, render_factors


class AssetDepartModelFolder(BaseFolder):

    @classmethod
    def is_applicable(cls, folderpath:str)->bool:
        return is_asset_depart_model_folder(folderpath)

    def __init__(self, path: str):
        super().__init__(path)
        self._folder_type = FolderType.ASSET_DEPART_MODEL

    
    def is_preview(self, file_path: str):
        """是否為預覽圖

        - preview 檔所在地至少要有一層目錄
        - preview 檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是 preview 檔的檔名叫做 "preview"
        - preview 檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
        """

        asset_pathobj = PureWindowsPath(file_path)

        if not asset_pathobj.parent.name:
            return False

        if not util.validate_tex_extension(file_path):
            return False

        path_parts = asset_pathobj.parts
        file_name = path_parts[-1].lower()
        parent_name = path_parts[-2].lower()
        if parent_name in file_name:
            return True

        if any([i in file_path for i in preview_factors]):
            return True
        return False


    def is_render_image(self, file_path: str) -> bool:
        """是否為渲染圖

        - 渲染圖檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是渲染圖檔的檔名叫做 "render"
        - 渲染圖檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
        """

        asset_pathobj = PureWindowsPath(file_path)

        if not asset_pathobj.parent.name:
            return False
        
        if not util.validate_tex_extension(file_path):
            return False

        path_parts = asset_pathobj.parts

        for render_factor in render_factors:
            for path_part in path_parts:
                if render_factor.lower() == path_part.lower():
                    return True
        return False


def is_asset_depart_model_folder(folder_path: str):
    """判斷是否為 FolderType.ASSET_DEPART_MODEL"""
    folder_required = ["Model", "Texture", "Render"]
    items = util.list_dir(folder_path)
    items = [i.lower() for i in items]
    if not all([i.lower() in items for i in folder_required]):
        return False
    return True