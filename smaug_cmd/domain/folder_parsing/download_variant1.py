import os
import re
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.domain.upload_strategies import DownloadVariant1UploadStrategy




class DownloadVariant1Folder(BaseFolder):
    def __init__(self, path: str, upload_strategy:DownloadVariant1UploadStrategy):
        super().__init__(path, upload_strategy)
        self._type_folder = FolderType.DOWNLOAD_VARIANT1_MODEL

    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        return is_download_variant1_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        # 確認是否是圖檔
        if not util.validate_tex_extension(file_path):
            return False
        # 是否在主目錄下
        return os.path.dirname(file_path) == self._path

    def is_render_image(self, file_path: str) -> bool:
        """目前沒有渲染圖"""
        return False

    def is_model(self, file_path: str) -> bool:
        if not util.validate_model_extension(file_path):
            return False
        return True

    def is_texture(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        return True


def is_download_variant1_model_folder(folder_path: str):
    """判斷是否為下載變體資料夾
    下載變體1資料夾的特色是 base dir 下數個以 `uploads_files_` 開頭的資料夾，內含貼圖跟 dcc 檔，該資料夾的名稱 `+` 替代 ` `(空白)
    並於 base dir 也有 preview 圖片

    example:
        _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
        _Asset\MoonshineProject_2020_Obsidian\202001_AsusBrandVideo4\Buy\Sci+Fi+Power+Suit
    """

    # base_name = os.path.basename(folder_path)
    pattern = re.compile(r"^uploads_files_\d+_[\w\+ -]+$")
    items = util.list_dir(folder_path)
    for item in items:
        if pattern.match(item):
            return True
    return False