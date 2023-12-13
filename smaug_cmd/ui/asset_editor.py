from typing import Optional, Callable
import logging
from PySide6.QtWidgets import QWidget
from smaug_cmd.designer.asset_editor_ui import Ui_asset_editor_wgt
from smaug_cmd.ui.category_widgets import CategoryListWidget
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.adapter.images import ImageHandler
from smaug_cmd.adapter.smaug import SmaugJson
from smaug_cmd.adapter.cmd_handlers.asset import asset_categories

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
        self._asset = asset
        self._sjson = (
            SmaugJson(self._asset["basedir"]) if self._asset is not None else None
        )
        self.breadcrumb_cb = breadcrumb_cb
        self.cate_picker_btn.clicked.connect(self._on_cate_picker_btn_clicked)
        self.tags_widget.tagsChanged.connect(self._on_tag_changed)
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
        if self._asset is None:
            self.asset_name_lbl.setText("New Asset")
            self.asset_name_lbl.setEnabled(False)
            return
        self.asset_name_lbl.setEnabled(True)
        self.asset_name_lbl.setText(self._asset["name"])
        asset_name = self._asset["name"]
        if self._asset["name"] == "":
            asset_name = "New Asset"
        self.asset_name_lbl.setText(asset_name)
        return

    def __update_asset_id(self):
        if self._asset is None:
            self.asset_id_lbl.setText("Id: None")
            return
        self.asset_id_lbl.setText(f'Id: {str(self._asset["id"])}')
        return

    def __update_breadcrumb(self):
        if (
            self._asset is None
            or self.breadcrumb_cb is None
            or self._asset["categoryId"] is None
        ):
            self.asset_cate_lbl.setText("Category: None")
            self.asset_cate_lbl.setEnabled(False)
            return
        self.asset_cate_lbl.setEnabled(True)
        self.breadcrumb_cb(
            self._asset["categoryId"], self.asset_cate_lbl, self.cate_picker_btn
        )
        return

    def __update_previews(self):
        if self._asset is None:
            # dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.preview_widget.clear()
            self.preview_widget.setEnabled(False)
            return

        self.setEnabled(True)
        self.preview_widget.setPictures(self._asset["previews"])

        cached_preview = self.__make_preview()
        if cached_preview != "":
            self.asset_info_frame.setStyleSheet(
                f'#asset_info_frame {{ background-image: url("{cached_preview}");'
                "background-repeat: no-repeat;"
                "background-position: center;}}"
            )
        else:
            self.asset_info_frame.setStyleSheet(
                "#asset_info_frame { background-image: url(:/ui/no_preview.png);}"
            )
        return

    def __update_renders(self):
        if self._asset is None:
            # dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # no_picture = os.path.join(dir_base, "resource", "no_picture.png")
            self.render_widget.clear()
            self.setEnabled(False)
            return
        self.preview_widget.setEnabled(True)
        self.render_widget.setPictures(self._asset["renders"])
        return

    def __update_tags(self):
        if self._asset is None:
            self.tags_widget.clear()
            self.tags_widget.setEnabled(False)
            return

        self.tags_widget.setEnabled(True)
        tags = self._asset["tags"]
        self.tags_widget.clear()
        for tag in tags:
            self.tags_widget.addTag(tag)
        return

    def __update_model_files(self):
        if self._asset is None:
            self.model_widget.setEnabled(False)
            self.model_widget.clear()
            return
        self.model_widget.setEnabled(True)
        files = self._asset["models"]
        self.model_widget.clear()
        self.model_widget.setFiles(files)
        return

    def __update_texture_files(self):
        if self._asset is None:
            self.textures_widget.setEnabled(False)
            self.textures_widget.clear()
            return
        self.textures_widget.setEnabled(True)
        files = self._asset["textures"]
        self.textures_widget.clear()
        self.textures_widget.setFiles(files)
        return

    def setAsset(self, asset: AssetTemplate):
        self._asset = asset
        self._sjson = SmaugJson(asset["basedir"])
        data = self._sjson.deserialize()
        self._asset.update(data)
        self._update_ui()
        return

    def __make_preview(self):
        if self._asset is None:
            logger.warning("Asset is None")
            return ""
        preview_filepath = self._asset["previews"][0] if self._asset["previews"] else None
        if preview_filepath is None:
            return ""
        asset_dir = self._asset["basedir"]
        cached_preview = ImageHandler.make_thumbnail(asset_dir, preview_filepath)
        cached_preview_filepath = asset_dir + "/.smaug/preview.png"
        cached_preview.save(cached_preview_filepath)
        return cached_preview_filepath

    def _on_cate_picker_btn_clicked(self):
        # 從 api 取得 category 的資料
        home_menutree = asset_categories()

        # 顯示 CategoryListWidget
        cate_win = CategoryListWidget(parent=self)
        cate_win.categoryIdChanged.connect(self._on_cate_id_selected)
        cate_win.addMenuTree(home_menutree)
        cate_win.show()

    def _on_cate_id_selected(self, cate_id: int):
        logger.debug(f"Category Id: {cate_id}")
        if self._asset is None:
            logger.warning("Asset is None")
            return
        self._asset["categoryId"] = cate_id
        if self._sjson is not None:
            with self._sjson:
                self._sjson["categoryId"] = cate_id
        self.__update_breadcrumb()
        return

    def setBreadcrumb_cb(self, cb: Callable):
        self.breadcrumb_cb = cb
        return

    def _on_tag_changed(self, tags: list):
        if self._asset is None:
            logger.warning("Asset is None")
            return
        self._asset["tags"] = tags
        if self._sjson is not None:
            with self._sjson: 
                self._sjson["tags"] = tags
        return

    def asset(self):
        return self._asset

    # 補 id 在 smaug.json 的部份
