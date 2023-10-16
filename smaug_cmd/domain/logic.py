import logging
from typing import List, Optional, Tuple, Callable
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QPushButton

from smaug_cmd.domain.smaug_types import Menu, MenuTree, AssetTemplate
from smaug_cmd.model import login_in as api_login
from smaug_cmd.model import data as ds
from smaug_cmd.domain import parsing as ps


logger = logging.getLogger('smaug-cmd.domain')


class SmaugCmdHandler(QObject):
    
    def __init__(self):
        super().__init__(None)

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb if er_cb(error_msg) else None

    def log_in(self, user_name, password) -> Tuple[int, dict]:
        return api_login(user_name, password)

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

    def create_asset(self, asset_template: AssetTemplate):
        asset_id = ds.create_asset(asset_template)

        