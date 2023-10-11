from typing import List
from PySide6.QtWidgets import QWidget
from smaug_cmd.designer.asset_editor_ui import Ui_asset_editor_wgt
from smaug_cmd.domain.smaug_types import AssetTemplate


class AssetEditorWidget(QWidget, Ui_asset_editor_wgt):
    def __init__(self, compose_cate_breadcrumb, parent=None, asset:AssetTemplate=None):
        super(AssetEditorWidget, self).__init__(parent)
        self.setupUi(self)
        self.asset=asset
        self._compose_cate_breadcrumb=compose_cate_breadcrumb
        self._update_ui()
    
    def _update_ui(self):
        if self.asset is None:
            return
        
        self.asset_name_lbl.setText(self.asset.name)
        self.asset_id_lbl.setText(self.asset.id)

        self._compose_cate_breadcrumb(self.asset['categoryId'], self.asset_cate_lbl, self.catePicker_btn)


        self.__update_tags(self.asset['tags'])
    
    def __update_tags(self, tags:List[str]):
        self.tags_widget.clear()
        for tag in tags:
            self.tags_widget.addTag(tag)
