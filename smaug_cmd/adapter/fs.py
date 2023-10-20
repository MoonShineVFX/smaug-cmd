import zipfile
import tempfile
from typing import List
import os

def create_temp_zip_from_files(file_paths: List[str], file_name:str=None) -> str:
    temp_file_name = ""
    # 創建一個暫存文件，這裡使用 with 語句以確保文件會被適當地關閉
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
        # 使用 zipfile 庫將文件添加到 ZIP 檔案
        with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                base_name = file_path.split('/')[-1]
                zipf.write(file_path, base_name)
        
        # 儲存暫存 ZIP 檔案的路徑
        temp_file_name = temp_file.name

     # 如果有提供 file_name，則重新命名暫存文件
    if file_name:
        new_file_path = os.path.join(os.path.dirname(temp_file_name), file_name)
        os.rename(temp_file_name, new_file_path)
        temp_file_name = new_file_path
    
    # 返回暫存 ZIP 檔案的路徑
    return temp_file_name