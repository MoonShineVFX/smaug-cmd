from typing import Optional, Callable
import os
from PySide6.QtWidgets import QWidget
from smaug_cmd.designer.asset_editor_ui import Ui_asset_editor_wgt
from smaug_cmd.domain.smaug_types import AssetTemplate


class AssetEditorWidget(QWidget, Ui_asset_editor_wgt):
    def __init__(
        self,
        parent=None,
        asset: Optional[AssetTemplate] = None,
        breadcrumb_cb: Optional[Callable] = None,
    ):
        super(AssetEditorWidget, self).__init__(parent)
        self.setupUi(self)
        self.asset = asset
        self.breadcrumb_cb = breadcrumb_cb
        self._update_ui()

    def _update_ui(self):
        self.__update_asset_name()
        self.__update_asset_id()
        self.__update_breadcrumb()
        self.__update_previews()
        self.__update_renders()
        self.__update_tags()
        return

    def __update_asset_name(self):
        if self.asset is None:
            self.asset_name_lbl.setText("New Asset")
            self.asset_name_lbl.setEnabled(False)
            return
        self.asset_name_lbl.setEnabled(True)
        self.asset_name_lbl.setText(self.asset["name"])
        asset_name = self.asset["name"]
        if self.asset["name"] == "":
            asset_name = "New Asset"
        self.asset_name_lbl.setText(asset_name)
        return

    def __update_asset_id(self):
        if self.asset is None:
            self.asset_id_lbl.setText("Id: None")
            return
        self.asset_id_lbl.setText(f'Id: {str(self.asset["id"])}')
        return

    def __update_breadcrumb(self):
        if self.asset is None or self.breadcrumb_cb is None:
            self.asset_cate_lbl.setText("Category: None")
            self.asset_cate_lbl.setEnabled(False)
            return
        self.asset_cate_lbl.setEnabled(True)
        self.breadcrumb_cb(
            self.asset["categoryId"], self.asset_cate_lbl, self.cate_picker_btn
        )
        return

    def __update_previews(self):
        if self.asset is None:
            dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.preview_widget.setPictures(no_picture)
            self.preview_widget.setEnabled(False)
            return
        self.setEnabled(True)
        self.preview_widget.setPictures(self.asset["previews"])
        return

    def __update_renders(self):
        if self.asset is None:
            dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.render_widget.setPictures(no_picture)
            self.setEnabled(False)
            return
        self.preview_widget.setEnabled(True)
        self.render_widget.setPictures(self.asset["renders"])
        return

    def __update_tags(self):
        if self.asset is None:
            self.tags_widget.setEnabled(False)
            self.tags_widget.clear()
            return
        self.tags_widget.setEnabled(True)
        tags = self.asset["tags"]
        self.tags_widget.clear()
        for tag in tags:
            self.tags_widget.addTag(tag)
        return

    def setAsset(self, asset: AssetTemplate):
        self.asset = asset
        self._update_ui()
        return
