import logging
from typing import List, Optional, Tuple, Callable
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QPushButton

from smaug_cmd.domain.smaug_types import Menu, MenuTree, AssetTemplate, Representation
from smaug_cmd.model import login_in as api_login
from smaug_cmd.model import data as ds
from smaug_cmd.domain import parsing as ps
from smaug_cmd.adapter import remote_fs as rfs


logger = logging.getLogger('smaug-cmd.domain')


class SmaugCmdHandler(QObject):
    
    def __init__(self):
        super().__init__(None)
        self.current_user = None

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb if er_cb(error_msg) else None

    def log_in(self, user_name, password) -> Tuple[int, dict]:
        re = api_login(user_name, password)
        if str(re[0])[0] == '2':
            self.current_user = re[1]
        return re

    def get_menus(self, error_cb: Optional[Callable]) -> Optional[List[Menu]]:
        re = ds.get_menus()
        if str(re[0])[0] != '2':
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def get_menu_tree(self, menu_id, error_cb: Optional[Callable] = None) -> Optional[MenuTree]:
        re = ds.get_menu_tree(menu_id)
        if str(re[0])[0] != '2':
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]
    
    def _setup_cate_breadcrumb(self, cate: int, cate_lbl: QLabel, cate_picker_btn: QPushButton):
        '''Compose the category breadcrumb.'''
        # 取的分類的父分類
        cate_query = ds.get_category(cate)
        if str(cate_query[0])[0] != 2:
            self.error_handler(cate_query[1]["message"])
            return
        cate_detail = cate_query[1]
        
        # 設定 UI
        cate_lbl.setText(f"category: {cate_detail['breadCrumb']}")
        cate_picker_btn.setProperty("smaug_cate", True)
        return
    
    def asset_template(self, folder_path):
        # convert folder to asset template
        asset_template = ps.folder_asset_template(folder_path)
        return asset_template

    def create_asset_proc(self, asset_template: AssetTemplate):
        """在資料庫建立 asset 的流程
        會處理模型檔跟貼圖檔的分類之後壓縮成 zip 檔案
        各別上傳完 zip 檔之後再去資料庫建立 representation
        """

        
        # 如果有 fbx 或是 usd 檔，用他們收集詮釋資料(檔案大小、bounding box，點數，面數等)
        usd_file = ps.find_usd(asset_template['models'])
        if usd_file:
            usd_meta = ps.usd_meta(usd_file)
            asset_template['meta'].update(usd_meta)
        # 建立 asset 以取得 asset id
        asset_id = ds.create_asset(asset_template)
        asset_name = asset_template["name"]
        
        representations = list()
        # _preview_picture_process
        representations.extend([
            self._upload_preview_picture_process(asset_id, asset_name, preview_file, idx)
            for idx, preview_file in enumerate(asset_template["previews"])
        ])

        # splite textures to texture-group, 
        texture_groups = ps.texture_group(asset_id, asset_template["textures"])
        # generate texture zip file
        zipped_textures = dict()
        for key, files in texture_groups.items():    
            zipped_file = ps.generate_zip(asset_name, key, files)
            zipped_textures["key"] = zipped_file
        uploaded_texture_object_names = rfs.put_textures(asset_id, zipped_textures)
        texture_ids = ds.create_textures(asset_id, uploaded_texture_object_names, meta={"Texture_Res":uploaded_texture_object_names.keys()})

        # splite models to model-group,
        model_groups = ps.model_group(asset_id, asset_template["models"])
        # generate model zip 
        zipped_models = dict()
        for key, files in model_groups.items():
            zip_file = ps.generate_zip(asset_name, key, files)
            zipped_models["key"] = zip_file
        uploaded_model_object_names = rfs.put_models(asset_id, zipped_models)
        ds.create_representation(asset_id, uploaded_model_object_names, texture_ids)

        # upload preview model process
        # upload textures process
        # upload models process
        # upload renders process
        # update meta data, find bounding box, find texture size, find model size..., etc.
        # update tags

    def _upload_preview_picture_process(self, asset_id, asset_name, preview_file, idx) -> Representation:
        # upload preview picture
        file_name = os.path.basename(preview_file).split('.')[0]
        file_extension = os.path.splitext(preview_file)[-1].lower()
        object_name = f"/{asset_id}/{asset_name}_preview-{idx}{file_extension}"
        upload_previews_object_name = rfs.put_file(preview_file, object_name)

        # 收整要建立 REPRESENTATION 的資料
        preview_representation:Representation = {
            "assetId":asset_id,
            "name": file_name,
            "type":"PREVIEW",
            "format":"IMG",
            "fileSize": os.path.getsize(preview_file),
            "uploaderId": self.current_user["id"],
            "path": upload_previews_object_name
        }
        return preview_representation
    
