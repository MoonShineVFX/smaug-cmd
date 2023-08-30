from typing import List, Dict
import os
from pprint import pprint
from pathlib import Path, PureWindowsPath
from smaug_cmd.setting import texture_extensions, texture_factors, preview_factors, render_factors, model_extensions


i_asset_template = Dict[str, str | List[str]]


def _validate_extension(file_path: str):
    ''' 檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    '''
    if file_path.split('.')[-1].lower() in texture_extensions:
        return True
    return False


def model_classifier_extension(file_path: str) -> float:
    ''' 檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    '''
    if file_path.split('.')[-1].lower() in model_extensions:
        return True
    return False 


def is_texture(file_path: str):

    if not _validate_extension(file_path):
        return False
    
    if any([i in file_path.lower() for i in texture_factors]):
        return True
    return False


def is_preview(file_path: str):
    ''' 是否為預覽圖

    - preview 檔所在地至少要有一層目錄
    - preview 檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是 preview 檔的檔名叫做 "preview"
    - preview 檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
    '''
    
    asset_pathobj =  PureWindowsPath(file_path)

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
    ''' 是否為渲染圖

    - 渲染圖檔的名字裡有包含完整的目錄名(都先轉成小寫比對)或是渲染圖檔的檔名叫做 "render"
    - 渲染圖檔是合法的圖案，合法圖檔副檔名在 setting 中有列表
    '''

    asset_pathobj =  PureWindowsPath(file_path)

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
    if file_path.split('.')[-1].lower() in model_extensions:
        return True
    return False


def directory_to_json(path: str):
    ''' 將資料夾轉成 json 格式'''

    asset_pathobj = Path(path)
    pprint(list(asset_pathobj.iterdir()))

    asset_template:i_asset_template = {
        "preview_pic": "",
        "preview_model": "",
        "models": [],
        "textures": [],
        "meta" :{}
    }
    return asset_template

    # for root, _, filenames in os.walk(path):
    #     for filename in filenames:
    #         print(os.path.join(root, filename))


if __name__ == '__main__':
    directory_to_json('/home/deck/repos/smaug/storage/_source/Tree_A/')