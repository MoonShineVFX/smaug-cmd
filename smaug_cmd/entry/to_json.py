from typing import List, Dict, Optional
import os
from pprint import pprint
from pathlib import Path, PureWindowsPath
from smaug_cmd.setting import texture_extensions, texture_factors, preview_factors, render_factors, model_extensions


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


def guess_preview_model(file_paths: str) -> str | None:
    for file_path in file_paths:
        if file_path.split('.')[-1].lower() == 'glb':
            return file_path
    return None


i_asset_template = Dict[str, str | List[str]]

def directory_to_json(path: str):
    ''' 將資料夾轉成 json 格式'''

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

    asset_template:i_asset_template = {
        "previews": previews,
        "preview_model": preview_model,
        "models": models,
        "textures": textures,
        "meta" :metadata
    }

    return asset_template

    # for root, _, filenames in os.walk(path):
    #     for filename in filenames:
    #         print(os.path.join(root, filename))


if __name__ == '__main__':
    if os.name == 'nt':
        re = directory_to_json('D:/repos/smaug-cmd/_source/Tree_A/')
    else:
        re = directory_to_json('/home/deck/repos/smaug/storage/_source/Tree_A/')
    pprint(re)