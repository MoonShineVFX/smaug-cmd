import os
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.domain.upload_strategies.taiwan_culture import (
    TaiwanCultureUploadStrategy,
)


class TaiwanCultureResourceModelFolder(BaseFolder):
    def __init__(self, path: str, upload_strategy: TaiwanCultureUploadStrategy):
        super().__init__(path, upload_strategy)
        self._folder_type = FolderType.TAIWAN_CULTURE_MODEL

    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        return is_taiwan_culture_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        if os.path.basename(os.path.dirname(file_path)) != self._at["name"]:
            return False
        return file_path.lower().split()[0].endswith("preview")

    def is_render_image(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        if os.path.basename(os.path.dirname(file_path)) != "Render":
            return False
        return True

    def is_model(self, file_path: str) -> bool:
        if not util.validate_model_extension(file_path):
            return False
        if os.path.basename(os.path.dirname(file_path)) != self._at["name"]:
            return False
        return True

    def is_texture(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False
        if os.path.basename(os.path.dirname(file_path)).lower() not in [
            "texture",
            "texture_jpg",
        ]:
            return False
        return True


def is_taiwan_culture_model_folder(folder_path: str) -> bool:
    """判斷是否為 ResourceFolderType.TAIWAN_CULTURE_MODEL 資料夾"""
    # 有 3D 目錄
    # 有 texture 目錄 (有時會有 Texture_JPG 目錄)
    # 有 Preview 目錄
    # 有 Render 目錄
    folder_required = ["3D", "Texture", "Preview", "Render"]

    items = util.list_dir(folder_path)
    items = [i.lower() for i in items]
    for folder in folder_required:
        if folder.lower() not in items:
            return False

    return True
