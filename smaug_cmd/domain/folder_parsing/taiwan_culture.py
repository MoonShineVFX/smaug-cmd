from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType


class TaiwanCultureResourceModelFolder(BaseFolder):
    def __init__(self, path: str):
        super().__init__(path)
        self._folder_type = FolderType.TAIWAN_CULTURE_MODEL

    @classmethod
    def is_applicable(cls, folderpath:str)->bool:
        return is_taiwan_culture_model_folder(folderpath)


def is_taiwan_culture_model_folder(folder_path: str) -> bool:
    """判斷是否為 ResourceFolderType.TAIWAN_CULTURE_MODEL 資料夾"""
    # 有 3D 目錄
    # 有 texture 目錄
    # 有 Preview 目錄
    # 有 Render 目錄
    folder_required = ["3D", "Texture", "Preview", "Render"]
    
    items = util.list_dir(folder_path)
    items = [i.lower() for i in items]
    for folder in folder_required:
        if folder.lower() not in items:
            return False

    return True