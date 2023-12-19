import os
from typing import List
from smaug_cmd.domain.exceptions import SmaugApiError


def list_dir(folder_path) -> List[str]:
    try:
        items = os.listdir(folder_path)
    except Exception as e:
        raise SmaugApiError(f"Reading Folder({folder_path}) Error: {e}")
    return items