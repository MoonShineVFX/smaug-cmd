# -*- coding: utf-8 -*-
import logging
from typing import Optional 
from PySide6.QtCore import QSettings, QDir
from PySide6.QtWidgets import QDialog, QMessageBox

from smaug_cmd.designer.asset_list_ui import Ui_asset_list_dlg
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.services import SmaugCmdLogic

logger = logging.getLogger("smaug-cmd.ui.asset_list")


class AssetListDialog(QDialog, Ui_asset_list_dlg):
    _section_name= "smaugAssetListDialog"

    def __init__(
        self,
        parent=None,
        to_asset_template_cb=None,
        logic: Optional[SmaugCmdLogic] = None,
        setting: Optional[QSettings] = None,
    ):
        super(AssetListDialog, self).__init__(parent)
        self.setupUi(self)
        self.to_asset_template_cb = to_asset_template_cb
        self.folder_tree_widget.selectedFolder.connect(self._on_folder_selected)
        self.push_db_btn.pressed.connect(self._on_push_db_pressed)
        self.folder_picker_widget.folderSelected.connect(self._on_root_folder_selected)
        self.logic = logic
        self._setting = setting
        if self.logic is not None:
            # self.to_asset_template_cb = self.logic.asset_template
            self.asset_widget.asset_page.setBreadcrumb_cb(self.logic.cate_breadcrumb)
            self.push_db_btn.pressed.connect(self._on_push_db_pressed)

        self._read_settings()

    def _read_settings(self):
        if self._setting is None:
            self.folder_tree_widget.setRootFolder(str(QDir.homePath()))
            return
        root_folder = self._setting.value(self._section_name +"/rootFolder", None)
        if root_folder is None:
            self.folder_tree_widget.setRootFolder(str(QDir.homePath()))
        else:
            self.folder_tree_widget.setRootFolder(str(root_folder))
        return

    def _on_folder_selected(self, path):
        if self.logic is None:
            return
        try:
            asset_template = self.logic.asset_template(path)
        except SmaugError as e:
            QMessageBox.critical(self, "還沒支援回收組的格式", str(e))
            asset_template = None
        self.asset_widget.setAsset(asset_template)
        return

    def _on_root_folder_selected(self, path):
        self.folder_tree_widget.setRootFolder(path)
        if self._setting:
            self._setting.setValue("rootFolder", path)
        return

    def setToAssetTemplateCallback(self, cb):
        self.to_asset_template_cb = cb
        return

    def _on_push_db_pressed(self):
        logger.info("push to db pressed")
        asset_template = self.asset_widget.asset()
        if asset_template is None:
            QMessageBox.critical(self, "上傳失敗", "請先選擇有效 Asset 資料夾")
            return
        if self.logic is None:
            return
        try:
            self.logic.create_asset_proc(asset_template)
        except SmaugError as e:
            QMessageBox.critical(self, "上傳失敗", str(e))

    def closeEvent(self, event):
        self._write_settings()
        return super().closeEvent(event)
    
    def _write_settings(self):
        if self._setting is None:
            return
        key_root_folder = self._section_name + "/rootFolder"
        self._setting.setValue(key_root_folder, self.folder_tree_widget.rootFolder())
        return
