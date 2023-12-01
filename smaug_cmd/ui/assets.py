# -*- coding: utf-8 -*-
import logging
from PySide6.QtWidgets import QDialog
from smaug_cmd.designer.asset_list_ui import Ui_asset_list_dlg

logger = logging.getLogger("smaug-cmd.ui.asset_list")


class AssetListDialog(QDialog, Ui_asset_list_dlg):
    def __init__(self, parent=None, to_asset_template_cb=None, logic=None):
        super(AssetListDialog, self).__init__(parent)
        self.setupUi(self)
        self.to_asset_template_cb = to_asset_template_cb
        self.folder_tree_widget.selectedFolder.connect(self._on_folder_selected)
        self.push_db_btn.pressed.connect(self._on_push_db_pressed)
        self.folder_picker_widget.folderSelected.connect(self._on_root_folder_selected)
        self.logic = logic
        if logic is not None:
            self.to_asset_template_cb = self.logic.asset_template
            self.asset_widget.asset_page.setBreadcrumb_cb(logic.cate_breadcrumb)

    def _on_folder_selected(self, path):
        asset_template = self.to_asset_template_cb(path)
        self.asset_widget.setAsset(asset_template)
        return

    def _on_root_folder_selected(self, path):
        self.folder_tree_widget.setRootFolder(path)
        return

    def setToAssetTemplateCallback(self, cb):
        self.to_asset_template_cb = cb
        return

    def _on_push_db_pressed(self):
        logger.info("push to db pressed")
