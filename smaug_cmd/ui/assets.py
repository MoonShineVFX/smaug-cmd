# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog

from smaug_cmd.designer.asset_list_ui import Ui_asset_list_dlg


class AssetListDialog(QDialog, Ui_asset_list_dlg):
    def __init__(self, parent=None):
        super(AssetListDialog, self).__init__(parent)
        self.setupUi(self)
        self.to_asset_template_cb = None
        self.folder_tree_widget.selectedFolder.connect(self._on_folder_selected)
    
    def _on_folder_selected(self, path):
        asset_template = self.to_asset_template_cb(path)
        self.asset_editor_widget.setAsset(asset_template)
        return

    def setToAssetTemplateCallback(self, cb):
        self.to_asset_template_cb = cb
        return
