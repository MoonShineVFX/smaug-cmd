import zipfile
import tempfile
from typing import List
import os
import shutil


def create_temp_zip_from_files(file_paths: List[str], file_name:str=None) -> str:
    temp_file_name = ""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
        with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                base_name = file_path.split('/')[-1]
                zipf.write(file_path, base_name)
        
        # 儲存暫存 ZIP 檔案的路徑
        temp_file_name = temp_file.name

     # 如果有提供 file_name，則重新命名暫存文件
    if file_name:
        new_file_path = os.path.join(os.path.dirname(temp_file_name), file_name)
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        os.rename(temp_file_name, new_file_path)
        temp_file_name = new_file_path
    
    # 返回暫存 ZIP 檔案的路徑
    return temp_file_name


def collect_to_smaug(asset_base_dir, file_path):
    """將檔案移動到 smaug 資料夾"""
    # 如果檔案已經在 smaug 資料夾內，就不要再移動
    if ".smaug" in file_path:
        return
    # 如果檔案不在 smaug 資料夾內，就移動到 smaug 資料夾內
    file_name = os.path.basename(file_path)
    new_path = os.path.join(asset_base_dir, ".smaug", file_name)
    shutil.move(file_path, new_path)
    return new_path


