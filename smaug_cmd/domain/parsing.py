from typing import List, Dict, Literal
import os
from pprint import pprint
from pathlib import  PureWindowsPath
import requests
from smaug_cmd.setting import texture_extensions, texture_factors, preview_factors, render_factors, model_extensions
from smaug_cmd.domain.smaug_types import AssetTemplate


def _validate_extension(file_path: str):
    ''' 檢查副檔名是否合法

    - 副檔名在 setting 中有列表
    '''
    if file_path.split('.')[-1].lower() in texture_extensions:
        return True
    return False


def model_classifier_extension(file_path: str) -> bool:
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


    asset_template:AssetTemplate = {
        'name': '',
        "previews": previews,
        "preview_model": preview_model,
        "models": models,
        "textures": textures,
        "meta" :metadata
    }

    return asset_template

    # for root, _, filenames in os.walk(path):
    #     for filename in filenames:
    #         print(os.path.join(root, filename))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         rewq

def to_asset(folder_path: str):
    ''' 將資料夾轉成 asset json 格式'''

    # 資料夾轉成 json
    asset_json = directory_to_json(folder_path)
    # folder 名稱就是 asset 名稱
    asset_json.update({'name': os.path.basename(folder_path)})

    # 可以下載的 asset represation
    return asset_json


def to_asset_create_json(asset_json: AssetTemplate):
    ''' 將 asset json 格式 轉成 asset create api 用的 json 格式'''

    # 資料夾轉成 json
    
    # folder 名稱就是 asset 名稱
    asset_json['name'] = asset_json['name']
    asset_json['categoryId'] = asset_json.get('categoryId', 1)

    

    return asset_json

def upload_asset(asset_json: AssetTemplate):
    ''' 上傳 asset
    先建立 asset, 取得 asset id, 再上傳後續的東西
    '''
    asset_create_api = 'https://smaug-cmd.firebaseio.com' + '/api' + '/assets'
    representation_create_api = 'https://smaug-cmd.firebaseio.com' + '/api' + '/representations'

    asset_create_data = to_asset_create_json(asset_json)
    try:
        asset_create_resp = requests.post(asset_create_api, json=asset_create_data)
    except Exception as e:
        print(e)
        return None
    asset_data = asset_create_resp.json() 
    the_asset_id = asset_data['id']

    # 上傳 preview
    headers = { "content-type": "multipart/form-data" }
    for preview in asset_json['previews']:
        upload_preview_data = {
            "assetId": the_asset_id,
            "type": "preview"
        }
        # 依副檔名判斷是哪種 preview
        if preview.split('.')[-1].lower() in ['glb',]:
            
        try:
            requests.post(representation_create_api, headers=headers, json=upload_preview_data)
        except Exception as e:
            print(e)
            return None

    # 逼立


if __name__ == '__main__':
    if os.name == 'nt':
        re = to_asset('D:/repos/smaug-cmd/_source/Tree_A/')
    else:
        re = to_asset('/home/deck/repos/smaug/storage/_source/Tree_A/')
    pprint(re)