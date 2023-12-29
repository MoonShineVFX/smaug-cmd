import os
from pathlib import PureWindowsPath
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.upload_strategies import AvalonResourceUploader


class AvalonResourceFolder(BaseFolder):
    ava_folder = "_AvalonSource"

    def __init__(self, path: str, upload_strategies: AvalonResourceUploader):
        super().__init__(path, upload_strategies)
        self._type_folder = FolderType.AVALON_SOURCE_MODEL

    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        return is_avalon_source_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        # 確認是否是圖檔
        if not util.validate_tex_extension(file_path):
            return False

        # 確是上面不是 C D 之類的根目錄
        asset_pathobj = PureWindowsPath(file_path)
        if not asset_pathobj.parent.name:
            return False

        return True

    def is_render_image(self, file_path: str) -> bool:
        """目前沒有渲染圖"""
        return False

    def is_model(self, file_path: str) -> bool:
        if not util.validate_model_extension(file_path):
            return False

        for path_part in PureWindowsPath(file_path).parts:
            if self.ava_folder.lower() in path_part.lower():
                return True
        return False

    def is_texture(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        if file_path.find(self.ava_folder + "/texture"):
            return True
        return False


def is_avalon_source_model_folder(folder_path: str):
    """判是否為 ResourceFolderType.AVALON_SOURCE_MODEL 資料夾"""

    # 要有 _AvalonSource
    folder_required = "_avalonsource"
    for folder in util.list_dir(folder_path):
        if folder.lower() == folder_required:
            return True
    return False
