from typing import List, Dict
import os
from pprint import pprint
from pathlib import PureWindowsPath
from smaug_cmd.adapter import fs
from smaug_cmd.domain.exceptions import SmaugError

from smaug_cmd.setting import (
    texture_extensions,
    texture_factors,
    preview_factors,
    render_factors,
    model_extensions,
    exclude_files,
    exclude_folders
)
from smaug_cmd.domain.smaug_types import (
    AssetTemplate,
    AssetFolderType,
    RepresentationFormat,
    SOFTWARE_CATEGORIRS,
    REVERSE_SOFTWARE_CATEGORIRS,
    ResourceFolderType,
)


def format_from_softkey(soft_key: str) -> RepresentationFormat:
    """從軟體關鍵字取得格式"""
    if soft_key == "maya":
        return "MB"
    elif soft_key == "3dsmax":
        return "MAX"
    elif soft_key == "unreal":
        return "UNREAL"
    elif soft_key == "fbx":
        return "FBX"
    elif soft_key == "c4d":
        return "C4D"
    elif soft_key == "obj":
        return "OBJ"
    elif soft_key == "usd":
        return "USD"
    raise SmaugError(f"Unknow soft key: {soft_key}")


def is_asset_model_folder(path) -> AssetFolderType:
    """
    檢查指定的路徑是否為模型資料夾。

    參數:
        path (str): 要檢查的路徑。

    回傳:
        bool: 如果路徑是模型資料夾，則回傳 True, 否則回傳 False。
    """
    # 判斷是否為資源部資料夾(鍾墉)
    if is_resource_depart_folder(path):
        return AssetFolderType.RESOURCE_DEPART

    # 判斷是否為資產部資料夾(家家)
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


def find_usd(file_paths: List[str]) -> str | None:
    for file_path in file_paths:
        if is_usd(file_path):
            return file_path
    return None


def usd_meta(file_path: str):
    return {}  # todo: implement polycount, vertex count, face count, bounding box etc.


def guess_preview_model(file_paths: List[str]) -> str | None:
    for file_path in file_paths:
        if file_path.split(".")[-1].lower() == "glb":
            return file_path
    return None


# def load_dot_smaug(path: str)-> dict:
#     # location smaug.json file
#     smaug_json = os.path.join(path, ".smaug", "smaug.json")
#     if not os.path.exists(smaug_json):
#         return {}
#     with open(smaug_json, "r") as f:
#         smaug_data = f.read()

#     data = json.loads(smaug_data)
#     return data


def folder_asset_template(path: str) -> AssetTemplate:
    """將資料夾轉成 json 格式"""

    textures = []
    previews = []
    renders = []
    models = []
    metadata: dict = {}
    tags: List[str] = []

    for root, _, filenames in os.walk(path):
        for filename in filenames:
            # file_path = os.path.join(root, filename)
            file_path = root + "/" + filename
            if ".smaug" in file_path:
                continue
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
        "preview_model": preview_model if preview_model else "",
        "models": models,
        "textures": textures,
        "renders": renders,
        "meta": metadata,
        "tags": tags,
        "basedir": path,
        "createAt": None,
        "updateAt": None,
    }
    # sjson = SmaugJson(path)
    # data = sjson.deserialize()
    # asset_template.update(data)
    return asset_template


def categorize_files_by_keywords(
    files: List[str], keywords: List[str]
) -> Dict[str, List[str]]:
    categorized_files: Dict[str, List[str]] = {}
    for f in files:
        newf = f.replace("\\", "/")
        for keyword in keywords:
            if keyword in newf.split("/"):
                categorized_files.setdefault(keyword, []).append(newf)
    return categorized_files


def categorize_models( models: List[str]) -> Dict[str, List[str]]:
    categorized_models: Dict[str, List[str]] = {}
    for model in models:
        newf = model.replace("\\", "/")
        for keywords in SOFTWARE_CATEGORIRS.values():
            split_file = newf.split(".")
            if len(split_file) == 0:
                continue
            if split_file[-1] in keywords:
                softKey = REVERSE_SOFTWARE_CATEGORIRS[split_file[-1]]
                categorized_models.setdefault(softKey, []).append(newf)
    return categorized_models

def to_asset_create_paylad(asset_json: AssetTemplate):
    """將 asset json 格式 轉成 asset create api 用的 json 格式"""

    # 資料夾轉成 json

    # folder 名稱就是 asset 名稱
    asset_json["name"] = asset_json["name"]
    asset_json["categoryId"] = asset_json.get("categoryId", 1)

    return asset_json


def model_group(model_files: List[str]) -> Dict[str, List[str]]:
    return categorize_models(model_files)


def texture_group(texture_files: List[str]) -> Dict[str, List[str]]:
    keywords = ["2K", "4K"]
    return categorize_files_by_keywords(texture_files, keywords)


def generate_zip(asset_name, name_key, textures_files: List[str]) -> str:
    """將 textures 壓成 zip 檔案"""
    # 產生 zip 檔名
    zip_file_name = f"{asset_name}_{name_key}_texture.zip"
    zipped_file = fs.create_temp_zip_from_files(textures_files, zip_file_name)
    return zipped_file


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._folder_type = self._which_folder_type()
        self._mapping = {
            ResourceFolderType.NORMAL_SOURCE: NormalResourceFolder,
            ResourceFolderType.AVALON_SOURCE: AvalonResourceFolder,
            ResourceFolderType.DOWNLOAD_VARIANT1: DownloadVariant1ResourceFolder,
            ResourceFolderType.DOWNLOAD_VARIANT2: DownloadVariant2ResourceFolder,
            ResourceFolderType.THREE_MAX: ThreedMaxResourceFolder,
        }

    def _which_folder_type(self):
        if is_asset_depart_folder(self._path):
            return AssetFolderType.ASSET_DEPART
        elif is_resource_depart_folder(self._path):
            return AssetFolderType.RESOURCE_DEPART
        elif is_download_variant1_folder(self._path):
            return ResourceFolderType.DOWNLOAD_VARIANT1
        elif is_download_variant2_folder(self._path):
            return ResourceFolderType.DOWNLOAD_VARIANT2
        elif is_3dsmax_folder(self._path):
            return ResourceFolderType.THREE_MAX
        else:
            raise SmaugApiError("Unknown folder type")

    def create(self):
        return self._mapping[self._folder_type](self._path)




def is_avalon_source_folder(folder_path:str):
    '''判是否為 avalon source 資料夾
    其特色是目錄下會有 _AvalonSource 資料夾, 並帶有多張 preview 圖片
    _AvalonSource 下會有數個 texture 目錄，通常名為texture, texture_low, ...等等， 並包含多個 dcc 檔案
    dcc 檔可能有變體, 例加有後綴 _low 的模型檔案
    '''
    if not os.path.exists(f"{folder_path}\\_AvalonSource"):
        return False
    return True

def is_normal_folder(asset_templat:AssetTemplate):
    '''判斷是否為一般 asset 資料夾
    一般資料夾的特色是 base dir 下有一個貼圖目錄，名字可能為 Texture、tex，並且有多個 dcc 檔案, 同時也有複數 preview 圖片
    有時也會在 base dir 下有一個 Texture_JPG 資料夾，放置轉為 JPG 的貼圖檔案
    
    example: R:\_Asset\MoonshineProject_2019\BundleProject_TheBeltAndRoad\TheBeltAndRoad\Environment\ChangAnGate
    '''
    pass

def is_download_variant1_folder(base_dir): #3
    '''判斷是否為下載變體資料夾
    下載變體1資料夾的特色是 base dir 下數個以 `uploads_files_` 開頭的資料夾，內含貼圖跟 dcc 檔，該資料夾的名稱 `+` 替代 ` `(空白)
    並於 base dir 也有 preview 圖片

    example: 
        R:\_Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\parachute
        R:\_Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
    '''
    pass

def is_download_variant2_folder(asset_templat:AssetTemplate): #1
    '''判斷是否為下載變體資料夾第二型
    下載變體2資料夾的特色是 base dir 下有一個 `"asset 名稱"_textures` 的資料夾，內含貼圖，
    並於 base dir 下有多個 dcc 檔案, 同時也有複數 preview 圖片

    example: R:\_Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\parachute
    '''
    pass

def is_3dsmax_folder(asset_templat:AssetTemplate): #1
    '''判斷是否為 3ds max 資料夾
    3ds max 資料夾的特色是 base dir 下有一個名稱為 3d_Max 的資料夾，內含貼圖跟 dcc 檔，
    並於 base dir 下有多個 preview 檔案

    example: R:\_Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\DHQ
    '''
    pass


if __name__ == "__main__":
    if os.name == "nt":
        re = folder_asset_template("D:/repos/smaug-cmd/_source/Tree_A/")
    else:
        re = folder_asset_template("/home/deck/repos/smaug/storage/_source/Tree_A/")
    pprint(re)

# 暫時不知道該怎麼處理的資料夾內容
# R:\_Asset\MoonshineProject_2020_Obsidian\202001_AsusBrandVideo4\Buy\Sci+Fi+Power+Suit
# R:\_Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\Robot_Worker
# R:\_Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
# "R:\_Asset\MoonshineProject_2020_Obsidian\202006_VTidol\VTidol" 這個是內部帶有捷徑指向另一個真實存放檔案的資料夾