import os
import re
from typing import List, Dict

from smaug_cmd.adapter import fs
from smaug_cmd.domain.exceptions import SmaugApiError


from smaug_cmd.domain.smaug_types import (
    AssetTemplate,
    MdAsset,
    MdKanban,
    MdCategrory,
    MdJson,
    RepresentationFormat,
    SOFTWARE_CATEGORIRS,
    REVERSE_SOFTWARE_CATEGORIRS,
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
    elif soft_key == "blender":
        return "BLEND"
    raise SmaugApiError(f"Unknow soft key: {soft_key}")


# def is_asset_depart_folder(path) -> bool:
#     """
#     檢查指定的路徑下是否有 'texture', 'render', 'model' 這三個子目錄。

#     參數:
#         path (str): 要檢查的目錄路徑。

#     回傳:
#         bool: 如果目錄包含 'texture', 'Render', 'Model' 子目錄，則回傳 True, 否則回傳 False。
#     """
#     # 列出所有子目錄和文件
#     try:
#         dir_contents = os.listdir(path)
#     except FileNotFoundError:
#         print(f"The directory '{path}' does not exist.")
#         return False
#     except PermissionError:
#         print(f"Permission denied for directory '{path}'.")
#         return False

#     # 判斷是否包含 'texture', 'render', 'model' 子目錄
#     required_subdirs = {"Texture", "Render", "Model"}
#     actual_subdirs = {
#         item for item in dir_contents if os.path.isdir(os.path.join(path, item))
#     }

#     return required_subdirs.issubset(actual_subdirs)


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


def categorize_models(models: List[str]) -> Dict[str, List[str]]:
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


def md_parsing(md_file: str) -> MdJson:
    """解析 md 檔案，產生 md json 格式"""

    #yung
    # print ( 'md_file: ', md_file )


    md_json: MdJson = {
        "name": os.path.basename(md_file),
        "categories": md_parsing_categories(md_file),
        "assets": md_parsing_asset(md_file),
    }
    return md_json


def md_parsing_categories(md_path: str) -> List[MdCategrory]:
    # if "_Pic" in md_path:
    #     return []

    # Split the path into a list of directories
    dirs = md_path.split("/")

    # Remove unnecessary parts of the path
    dirs = dirs[dirs.index("MoonShineAsset") + 1 :]

    # Handle the file name
    file_name = dirs[-1]
    if file_name.endswith(".md"):
        file_name = file_name.replace(".md", "")
        file_name = file_name.split("_")[1]  # Get the part after 'Project 2019_'
        file_name = file_name.split(" ")[0]  # Remove 中文的部份
        dirs[-1] = file_name

    # Create a list of dictionaries
    categories: List[MdCategrory] = []
    for i in range(len(dirs)):
        categories.append(
            {"cate_name": dirs[i], "parent": dirs[i - 1] if i > 0 else None}
        )
    
    # Yung add
    # print ( 'categories: ', categories )

    return categories


def md_combine_categories(list1: List[Dict], list2: List[Dict]):
    combined = list1.copy()
    combined += [
        d
        for d in list2
        if not any(
            d["cate_name"] == x["cate_name"] and d["parent"] == x["parent"]
            for x in list1
        )
    ]
    return combined


def md_parsing_asset(md_file):
    """解析 asset md 檔案，產生 asset json 格式"""
    # 讀取 md 檔案
    with open(md_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    # 解析 md 檔案
    asset_json = md_parse_kanban_to_json(file_content)

    base_dir = os.path.dirname(md_file)
    base_dir = os.path.join(base_dir, "_Pic").replace("\\", "/")
    # update all preview path
    for asset in asset_json:
        for data in asset["data"]:
            data["previews"] = [
                os.path.join(base_dir, preview).replace("\\", "/")
                for preview in data["previews"]
            ]

    return asset_json


def md_parse_kanban_to_json(file_content: str) -> List[MdKanban]:
    """
    Parse the kanban file content to a structured JSON format.

    Args:
    - file_content (str): The content of the kanban file.

    Returns:
    - List[Dict[str, Any]]: A list of assets with their details in structured format.
    """
    assets: List[MdKanban] = []
    current_asset_name = ""
    asset_data: List[MdAsset] = []
    preview_pattern = re.compile(r"!\[\[([^]]+)\]\]")

    for line in file_content.split("\n"):
        if line.startswith("## "):
            # Save previous asset data if any
            if current_asset_name:
                asset_name, description = current_asset_name.split("<br>")
                asset_data[0]['description'] = description
                assets.append({"kanbon_name": asset_name.replace("_", " "), "data": asset_data})
                asset_data = []
            # Start new asset
            current_asset_name = line[3:].strip()

            # Yung Add
            # print ( 'current_asset_name: ', current_asset_name )

        elif line.startswith("- [ ]"):
            folder_match = re.search(r"\[Open Folder\]\(file://([^)]+)\)", line)
            previews = preview_pattern.findall(line)

            # print ( 'folder_match: ', folder_match )
            # print ( 'previews: ', previews )
            

            # Match the description by looking from the end of the line backwards to the first '<br>'
            tags_match = re.search(r"<br>([^<]+)$", line)

            
            if folder_match and tags_match:
                folder = folder_match.group(1)
                # 如果有 TEST_DATA_RESOURCE ，則用來取代 R:\_Asset
                test_data_resource = os.environ.get("TEST_DATA_RESOURCE")
                if test_data_resource is not None:
                    folder = folder.replace("R:/_Asset", test_data_resource).replace("\\", "/")

                    # # Yung add
                    # print ( 'folder: ',folder )

                    # image_paths = [os.path.join(folder,img) for img in  os.listdir(folder) if '.jpg' in img]
                    # previews = image_paths
                    # for img in image_paths:
                    #     print ( 'img: ', img )
                    # print ( '\n' )

                origin_tags = tags_match.group(1).strip()
                if origin_tags.endswith("]"):
                    origin_tags = ""
                if origin_tags:
                    tags_list = origin_tags.split("、")

                asset_data.append(
                    {"folder": folder, "previews": previews, "tags": tags_list, "description": ""}
                )

    # Append last asset
    if current_asset_name:
        asset_name, description = current_asset_name.split("<br>")
        asset_data[0]['description'] = description
        assets.append({"kanbon_name": asset_name.replace("_", " "), "data": asset_data})

    return assets


if __name__ == "__main__":
    from pprint import pprint
    test_data_resource = os.environ.get("TEST_DATA_RESOURCE")
    md_json = md_parsing(
        f"{test_data_resource}/_Obsidian/MoonShineAsset/Project 2019/Project2019_Nature 自然.md"
    )
    pprint(md_json)

# 暫時不知道該怎麼處理的資料夾內容
# R:\_Asset\MoonshineProject_2020_Obsidian\202001_AsusBrandVideo4\Buy\Sci+Fi+Power+Suit
# R:\_Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\Robot_Worker
# R:\_Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
# "R:\_Asset\MoonshineProject_2020_Obsidian\202006_VTidol\VTidol" 這個是內部帶有捷徑指向另一個真實存放檔案的資料夾
