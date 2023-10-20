from typing import List, Dict, Literal
import os
from pprint import pprint
from pathlib import PureWindowsPath

from smaug_cmd.adapter import fs

from smaug_cmd.setting import (
    texture_extensions,
    texture_factors,
    preview_factors,
    render_factors,
    model_extensions,
)
from smaug_cmd.domain.smaug_types import (
    AssetTemplate,
    AssetFolderType,
    TEXTURE_GROUP_KEYWORDS,
    SOFTWARE_CATEGORIRS
)


def is_asset_model_folder(path) -> AssetFolderType:
    """
    檢查指定的路徑是否為模型資料夾。

    參數:
        path (str): 要檢查的路徑。

    回傳:
        bool: 如果路徑是模型資料夾，則回傳 True, 否則回傳 False。
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
        bool: 如果目錄包含 'texture', 'Render', 'Model' 子目錄，則回傳 True, 否則回傳 False。
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
    required_subdirs = {"Texture", "Render", "Model"}
    actual_subdirs = {
        item for item in dir_contents if os.path.isdir(os.path.join(path, item))
    }

    return required_subdirs.issubset(actual_subdirs)


def is_resource_depart_folder(path) -> bool:
    return False


def _validate_extension(file_path: str):
    """檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    """
    if file_path.split(".")[-1].lower() in texture_extensions:
        return True
    return False


def model_classifier_extension(file_path: str) -> bool:
    """檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    """
    if file_path.split(".")[-1].lower() in model_extensions:
        return True
    return False


def is_texture(file_path: str):
    if not _validate_extension(file_path):
        return False

    if any([i in file_path.lower() for i in texture_factors]):
        return True
    return False


def is_preview(file_path: str):
    """是否為預覽圖

    - preview 檔所在地至少要有一層目錄
    - preview 檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是 preview 檔的檔名叫做 "preview"
    - preview 檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
    """

    asset_pathobj = PureWindowsPath(file_path)

    if not asset_pathobj.parent.name:
        return False

    if not _validate_extension(file_path):
        return False

    path_parts = asset_pathobj.parts
    file_name = path_parts[-1].lower()
    parent_name = path_parts[-2].lower()
    if parent_name in file_name:
        return True

    if any([i in file_path for i in preview_factors]):
        return True
    return False


def is_render_image(file_path: str):
    """是否為渲染圖

    - 渲染圖檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是渲染圖檔的檔名叫做 "render"
    - 渲染圖檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
    """

    asset_pathobj = PureWindowsPath(file_path)

    if not asset_pathobj.parent.name:
        return False

    if not _validate_extension(file_path):
        return False

    path_parts = asset_pathobj.parts

    for render_factor in render_factors:
        for path_part in path_parts:
            if render_factor.lower() == path_part.lower():
                return True
    return False


def is_model(file_path: str):
    if file_path.split(".")[-1].lower() in model_extensions:
        return True
    return False


def is_usd(file_path: str):
    """是否為 usd 檔案

    - usd 檔案的副檔名是 usd
    """
    if file_path.split(".")[-1].lower() == "usd":
        return True
    return False

def us_meta(file_path: str):
    
def find_usd(file_paths: List[str]) -> str | None:
    for file_path in file_paths:
        if is_usd(file_path):
            return file_path
    return None


def guess_preview_model(file_paths: str) -> str | None:
    for file_path in file_paths:
        if file_path.split(".")[-1].lower() == "glb":
            return file_path
    return None


def folder_asset_template(path: str) -> AssetTemplate:
    """將資料夾轉成 json 格式"""

    textures = []
    previews = []
    renders = []
    models = []
    metadata = {}

    for root, _, filenames in os.walk(path):
        for filename in filenames:
            os.path.join(root, filename)
            file_path = os.path.join(root, filename)
            if is_texture(file_path):
                textures.append(file_path)
            if is_preview(file_path):
                previews.append(file_path)
            if is_render_image(file_path):
                renders.append(file_path)
            if is_model(file_path):
                models.append(file_path)

    preview_model = guess_preview_model(models)

    asset_name = os.path.basename(path)
    asset_template: AssetTemplate = {
        "id": None,
        "name": asset_name,
        "categoryId": None,
        "previews": previews,
        "preview_model": preview_model,
        "models": models,
        "textures": textures,
        "renders": renders,
        "meta": metadata,
    }

    return asset_template


def categorize_files_by_keywords(texture_files: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    categorized_files = {}
    
    for keyword in keywords:
        # 使用列表推導式過濾出包含特定關鍵字的檔案
        filtered_files = [f for f in texture_files if keyword in f.split('/')]
        
        # 將過濾出的檔案存入字典中
        categorized_files[keyword] = filtered_files
    
    return categorized_files


def to_asset_create_paylad(asset_json: AssetTemplate):
    """將 asset json 格式 轉成 asset create api 用的 json 格式"""

    # 資料夾轉成 json

    # folder 名稱就是 asset 名稱
    asset_json["name"] = asset_json["name"]
    asset_json["categoryId"] = asset_json.get("categoryId", 1)

    return asset_json


def model_group(model_files: List[str])-> Dict[str, List[str]]:
    keywords = SOFTWARE_CATEGORIRS.keys()
    return categorize_files_by_keywords(model_files, keywords)


def texture_group(texture_files: List[str]) -> Dict[str, List[str]]:
    keywords = ["2K, 4K"]
    return categorize_files_by_keywords(texture_files, keywords)


def generate_zip(asset_name, name_key, textures_files: List[str]) -> str:
    """將 textures 壓成 zip 檔案"""
    # 產生 zip 檔名
    zip_file_name = f"{asset_name}_{name_key}_texture.zip"
    zipped_file = fs.create_temp_zip_from_files(textures_files, zip_file_name)
    return zipped_file


if __name__ == "__main__":
    if os.name == "nt":
        re = folder_asset_template("D:/repos/smaug-cmd/_source/Tree_A/")
    else:
        re = folder_asset_template("/home/deck/repos/smaug/storage/_source/Tree_A/")
    pprint(re)
