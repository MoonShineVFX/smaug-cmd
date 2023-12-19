from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder


def is_3dmax_model_folder(folder_path: str):  # 1
    """判斷是否為 3ds max 資料夾
    3ds max 資料夾的特色是 base dir 下有一個名稱為 3d_Max 的資料夾，內含貼圖跟 dcc 檔，
    並於 base dir 下有多個 preview 檔案

    example: _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\DHQ
    """
    items = util.list_dir(folder_path)
    if "3d_Max" not in items:
        return False
    return True


class ThreedMaxResourceModelFolder(BaseFolder):  # 2
    def __init__(self, path: str):
        super().__init__(path)

