import os
from typing import List
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.setting import texture_extensions, model_extensions


def list_dir(folder_path) -> List[str]:
    try:
        items = os.listdir(folder_path)
    except FileNotFoundError as e:
        raise SmaugApiError(f"The directory '{folder_path}' does not exist.") from e

    except PermissionError as e:
        raise SmaugApiError(f"Permission denied for directory '{folder_path}'.") from e

    return items


def validate_tex_extension(file_path: str):
    """檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    """
    if file_path.split(".")[-1].lower() in texture_extensions:
        return True
    return False


def validate_model_extension(file_path: str):
    """檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    """
    if file_path.split(".")[-1].lower() in model_extensions:
        return True
    return False
