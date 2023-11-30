from typing import Optional, Callable
import logging
from PySide6.QtWidgets import QWidget
from smaug_cmd.designer.asset_editor_ui import Ui_asset_editor_wgt
from smaug_cmd.ui.category_widgets import CategoryListWidget
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.adapter.images import ImageHandler

logger = logging.getLogger("smaug-cmd.ui.asset_editor")


class AssetEditorWidget(QWidget, Ui_asset_editor_wgt):
    def __init__(
        self,
        parent=None,
        asset: Optional[AssetTemplate] = None,
        breadcrumb_cb: Optional[Callable] = None,  # 這是組合 breadcrumb 的函式，由外部傳入
    ):
        super(AssetEditorWidget, self).__init__(parent)
        self.setupUi(self)
        self.asset = asset
        self.breadcrumb_cb = breadcrumb_cb
        self.cate_picker_btn.clicked.connect(self._on_cate_picker_btn_clicked)
        self._update_ui()

    def _update_ui(self):
        self.__update_asset_name()
        self.__update_asset_id()
        self.__update_breadcrumb()
        self.__update_previews()
        self.__update_renders()
        self.__update_tags()
        self.__update_model_files()
        self.__update_texture_files()
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
            # dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.preview_widget.clear()
            self.preview_widget.setEnabled(False)
            return

        self.setEnabled(True)
        self.preview_widget.setPictures(self.asset["previews"])

        cached_preview = self.__make_preview()
        if cached_preview != "":
            self.asset_info_frame.setStyleSheet(
                f'#asset_info_frame {{ background-image: url("{cached_preview}");'
                "background-repeat: no-repeat;"
                "background-position: center;}}"
            )
        else:
            self.asset_info_frame.setStyleSheet(
                "#asset_info_frame { background-image: none;}"
            )
        return

    def __update_renders(self):
        if self.asset is None:
            # dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.render_widget.clear()
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

    def __update_model_files(self):
        if self.asset is None:
            self.model_widget.setEnabled(False)
            self.model_widget.clear()
            return
        self.model_widget.setEnabled(True)
        files = self.asset["models"]
        self.model_widget.clear()
        self.model_widget.setFiles(files)
        return

    def __update_texture_files(self):
        if self.asset is None:
            self.textures_widget.setEnabled(False)
            self.textures_widget.clear()
            return
        self.textures_widget.setEnabled(True)
        files = self.asset["textures"]
        self.textures_widget.clear()
        self.textures_widget.setFiles(files)
        return

    def setAsset(self, asset: AssetTemplate):
        self.asset = asset
        self._update_ui()
        return

    def __make_preview(self):
        if self.asset is None:
            logger.warning("Asset is None")
            return ""
        preview_filepath = self.asset["previews"][0] if self.asset["previews"] else None
        if preview_filepath is None:
            return ""
        asset_dir = self.asset["basedir"]
        cached_preview = ImageHandler.make_thumbnail(asset_dir, preview_filepath)
        cached_preview_filepath = asset_dir + "/.smaug/preview.png"
        cached_preview.save(cached_preview_filepath)
        return cached_preview_filepath

    def setCategory(self, cate_id: int):
        if self.asset is None:
            logger.warning("Asset is None")
            return
        self.asset["categoryId"] = cate_id
        self.__update_breadcrumb()
        return

    def _on_cate_picker_btn_clicked(self):
        # 從 api 取得 category 的資料

        # 顯示 CategoryListWidget

        cate_win = CategoryListWidget()
        cate_win.addMenuTree()
        if self.breadcrumb_cb is None:
            logger.warning("Breadcrumb callback is None")
        else:
            if self.asset is not None:
                self.breadcrumb_cb(
                    self.asset["categoryId"], self.asset_cate_lbl, self.cate_picker_btn
                )
            else:
                logger.warning("Asset is None")
        return
