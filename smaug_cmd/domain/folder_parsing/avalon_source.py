from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder


class AvalonResourceModelFolder(BaseFolder):
    def __init__(self, path: str):
        super().__init__(path)
    
    @classmethod
    def is_applicable(cls, folderpath:str)->bool:
        return is_avalon_source_model_folder(folderpath)


def is_avalon_source_model_folder(folder_path: str):
    """判是否為 ResourceFolderType.AVALON_SOURCE_MODEL 資料夾"""

    # 要有 _AvalonSource
    folder_required = "_avalonsource"
    for folder in util.list_dir(folder_path):
        if folder.lower() == folder_required:
            return True
    return False