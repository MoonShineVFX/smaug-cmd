from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing._taiwan_culture import is_taiwan_culture_model_folder
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder


def is_normal_resource_model_folder(folder_path: str):
    """判斷是否為 ResourceFolderType.NORMAL_RESOURCE_MODEL
    這個規格跟 taiwan 有重疊，先確認是否為 taiwan 資料夾，如果是就不用再判斷是否為 normal 資料夾
    """
    
    if is_taiwan_culture_model_folder(folder_path):
        return False
    
    texture_folder_variant = ["Texture", "tex"]
    items = util.list_dir(folder_path)
    items = [i.lower() for i in items]
    if not any([i.lower() in items for i in texture_folder_variant]):
        return False
    return True


class NormalResourceModelFolder(BaseFolder):
    def __init__(self, path: str):
        super().__init__(path)