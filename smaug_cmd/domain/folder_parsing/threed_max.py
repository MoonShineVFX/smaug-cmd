import os
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType


class ThreedMaxResourceFolder(BaseFolder):
    def __init__(self, path: str, upload_strategy):
        super().__init__(path, upload_strategy)
        self.set_folder_type(FolderType.THREE_MAX_MODEL)

    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        return is_3dmax_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        return os.path.dirname(file_path).lower() == self._path.lower()

    def is_render_image(self, file_path: str) -> bool:
        """目前沒有渲染圖"""
        return False

    def is_model(self, file_path: str) -> bool:
        return util.validate_model_extension(file_path)

    def is_texture(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        return os.path.basename(os.path.dirname(file_path)).lower() == "texture"

def is_3dmax_model_folder(folder_path: str):
    """判斷是否為 3ds max 資料夾
    3ds max 資料夾的特色是 base dir 下有一個名稱為 3d_Max 的資料夾，內含貼圖跟 dcc 檔，
    並於 base dir 下有多個 preview 檔案

    example: _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\DHQ
    """
    items = util.list_dir(folder_path)
    if "3d_Max" not in items:
        return False
    return True