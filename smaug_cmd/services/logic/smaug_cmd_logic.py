import logging
from typing import List, Optional, Callable

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QPushButton

from smaug_cmd.domain.smaug_types import (
    Menu,
    MenuTree,
    AssetTemplate,
    UserInfo,
)
from smaug_cmd.model import login_in as api_login  # log_out as api_logout
from smaug_cmd.model import data as ds
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain.folder_class import FolderClassFactory

logger = logging.getLogger("smaug_cmd.domain")


class SmaugCmdLogic(QObject):
    def __init__(self):
        super().__init__(None)
        self._current_user: Optional[UserInfo] = None

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb(error_msg) if er_cb else None

    def log_in(self, user_name, password) -> bool:
        user = api_login(user_name, password)
        self._current_user = user
        return True

    def get_menus(self, error_cb: Optional[Callable]) -> Optional[List[Menu]]:
        re = ds.get_menus()
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def get_menu_tree(
        self, menu_id, error_cb: Optional[Callable] = None
    ) -> Optional[MenuTree]:
        re = ds.get_menu_tree(menu_id)
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def cate_breadcrumb(
        self, cate: int, cate_lbl: QLabel, cate_picker_btn: QPushButton
    ):
        """組合麵包屑"""
        # 取的分類的父分類
        cate_query = ds.get_category(cate, force=True)
        if str(cate_query[0])[0] != "2":
            self.error_handler(cate_query[1]["message"])
            return
        cate_detail = cate_query[1]

        # 設定 UI
        cate_lbl.setText(f"category: {cate_detail['breadCrumb']}")
        cate_picker_btn.setProperty("smaug_cate", True)
        return

    def asset_template(self, folder_path) -> Optional[AssetTemplate]:
        # convert folder to asset template

        self._folder_obj = FolderClassFactory(folder_path).create()
        if self._folder_obj is not None:
            return self._folder_obj.asset_template()
        return None

    def create_asset_proc(self, asset_template: AssetTemplate):
        """在資料庫建立 asset 的流程
        建立 asset 以取得 asset id 後
        會處理模型檔跟貼圖檔的分類之後壓縮成 zip 檔案
        各別上傳完 zip 檔之後再去資料庫建立 representation
        """
        # 檢查是否登入
        if self._current_user is None:
            raise SmaugError("Please login first.")
        if self._folder_obj is None:
            return
        self._folder_obj.upload_asset(asset_template, self._current_user)

    def update_asset_proc(self, asset_template: AssetTemplate):
        logger.debug("Update asset: %s", asset_template["name"])
