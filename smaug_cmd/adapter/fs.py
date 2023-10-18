import zipfile
import tempfile
from typing import List, Dict


def create_temp_zip_from_files(file_paths: List[str]) -> str:
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

    # 返回暫存 ZIP 檔案的路徑
    return temp_file_name


def categorize_files_by_keywords(texture_files: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    categorized_files = {}
    
    for keyword in keywords:
        # 使用列表推導式過濾出包含特定關鍵字的檔案
        filtered_files = [f for f in texture_files if keyword in f.split('/')]
        
        # 將過濾出的檔案存入字典中
        categorized_files[keyword] = filtered_files
    
    return categorized_files