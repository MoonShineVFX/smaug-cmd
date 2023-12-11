from typing import List
from smaug_cmd.adapter import fs


def create_zip(file_paths: List[str], file_name: str = None) -> str:
    """將 textures 壓成 zip 檔案"""
    # 產生 zip 檔名
    # if `file_name` end with no ".zip", add it.

    zip_file_name = f"{file_name}"
    zipped_file = fs.create_temp_zip_from_files(file_paths, zip_file_name)
    return zipped_file
