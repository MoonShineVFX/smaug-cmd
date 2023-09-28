import os
import logging
from typing import Callable, List
from smaug_cmd.domain.smaug_types import AssetFolderType


logger = logging.getLogger('fs')



def is_model_folder(path) -> AssetFolderType:
    """
    檢查指定的路徑是否為模型資料夾。

    參數:
        path (str): 要檢查的路徑。

    回傳:
        bool: 如果路徑是模型資料夾，則回傳 True，否則回傳 False。
    """
    # 判斷是否為資源部資料夾
    if is_resource_depart_folder(path):
        return AssetFolderType.RESOURCE_DEPART

    # 判斷是否為資產部資料夾
    if is_asset_depart_folder(path):
        return AssetFolderType.ASSET_DEPART

    return AssetFolderType.UNKNOWN


def is_asset_depart_folder(path) -> bool:
    """
    檢查指定的路徑下是否有 'texture', 'render', 'model' 這三個子目錄。

    參數:
        path (str): 要檢查的目錄路徑。

    回傳:
        bool: 如果目錄包含 'texture', 'Render', 'Model' 子目錄，則回傳 True，否則回傳 False。
    """
    # 列出所有子目錄和文件
    try:
        dir_contents = os.listdir(path)
    except FileNotFoundError:
        print(f"The directory '{path}' does not exist.")
        return False
    except PermissionError:
        print(f"Permission denied for directory '{path}'.")
        return False

    # 判斷是否包含 'texture', 'render', 'model' 子目錄
    required_subdirs = {'Texture', 'Render', 'Model'}
    actual_subdirs = {item for item in dir_contents if os.path.isdir(os.path.join(path, item))}

    return required_subdirs.issubset(actual_subdirs)


def is_resource_depart_folder(path) -> bool:
    return False


class TaskGroup:
    def __init__(self):
        self.tasks: List[Callable] = []

    def append_task(self, task: Callable):
        self.tasks.append(task)

    def run(self):
        for i, task in enumerate(self.tasks):
            try:
                task()
            except Exception as e:
                print(f"An error occurred while executing task {i}: {str(e)}")
                logger.error(f"An error occurred while executing task {i}: {str(e)}")