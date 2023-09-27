import os
from PySide6.QtCore import Qt, Signal, Slot, QSize, QModelIndex
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QProgressBar,
    QVBoxLayout,
    QFileDialog,
)
from . import AssetsTableView
from . import AssetRole, UploadModel


class BatchUploadWidget(QWidget):
    assets_folder = Signal(str)
    batch_upload_request = Signal(list)
    gen_thumbnail = Signal(str, str)

    def __init__(self, settings=None):
        super(BatchUploadWidget, self).__init__()
        self.setObjectName("batch_upload_widget")
        self._busy = False
        self.__msg_box = QMessageBox(parent=self)
        self.setWindowTitle(self.tr("Galaxy Uploader"))
        self.btn_browse_folder = QPushButton(self.tr("Select Folder"))
        self.btn_browse_folder.setObjectName("select_folder_button")
        self.btn_browse_folder.clicked.connect(self.__browse_folder)

        self.btn_reload = QPushButton(self.tr("Reload"))
        self.btn_reload.setObjectName("reload_button")
        self.btn_reload.setMaximumWidth(100)
        self.btn_reload.clicked.connect(self.reload)

        self.btn_clear = QPushButton(self.tr("Clear"))
        self.btn_clear.setObjectName("clear_button")
        self.btn_clear.setMaximumWidth(100)
        self.btn_clear.clicked.connect(self.clear_assets)

        btn_lay = QHBoxLayout()
        btn_lay.addWidget(self.btn_browse_folder)
        btn_lay.addWidget(self.btn_reload)
        btn_lay.addWidget(self.btn_clear)
        btn_lay.setStretchFactor(self.btn_browse_folder, 0.6)
        btn_lay.setStretchFactor(self.btn_reload, 0.2)
        btn_lay.setStretchFactor(self.btn_clear, 0.2)

        self.view_assets = AssetsTableView()
        self.view_assets.setObjectName("assets_view")
        self.view_assets.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.view_assets.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.view_assets.setAlternatingRowColors(True)
        self.view_assets.gen_thumbnail.connect(self._view_assets_gen_thumbnail)

        horizontalHeader = self.view_assets.horizontalHeader()
        horizontalHeader.setDefaultSectionSize(120)
        horizontalHeader.setStretchLastSection(True)

        verticalHeader = self.view_assets.verticalHeader()
        verticalHeader.setDefaultSectionSize(96)

        self._model = UploadModel()
        self.view_assets.setModel(self._model)
        self.view_assets.setIconSize(QSize(120, 96))

        self.bar_progress = QProgressBar()
        btn_batch_upload = QPushButton(self.tr("Upolad"))
        btn_batch_upload.clicked.connect(self.__send_request)
        btn_batch_upload.setDefault(True)
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)
        main_lay.addLayout(btn_lay)
        main_lay.addWidget(self.view_assets)
        main_lay.addWidget(btn_batch_upload)
        main_lay.addWidget(self.bar_progress)
        self.resize(QSize(1200, 400))
        #         self.setStyleSheet(qss)
        self.updateColumnSize()

    def __browse_folder(self):
        self._model.assets_folder = QFileDialog.getExistingDirectory()
        if self._model.assets_folder:
            self.btn_browse_folder.setText(self._model.assets_folder)
            self.assets_folder.emit(self._model.assets_folder)

    def __send_request(self):
        json_paths = [
            ast["json_path"]
            for ast in self._model.assets
            if ast["upload"] == Qt.CheckState.Checked
        ]
        self.batch_upload_request.emit(json_paths)

    def showText(self, text, title=None, modal=False):
        self.__msg_box.setText(text)
        if title:
            self.__msg_box.setWindowTitle(title)
        if modal:
            self.__msg_box.exec_()
        else:
            self.__msg_box.show()

    @Slot(dict)
    def set_assets(self, json_paths):
        """設定 assets"""
        self._model.append_assets(json_paths)

    @Slot(dict)
    def append_asset(self, json_path, stat=None):
        """設定 asset
        Args:
            json_path: json 檔路徑
            stat: AssetStats 物件屬性，代表該 asset 的異常狀態
        """
        self._model.append_asset(json_path, stat)

    @Slot()
    def clear_assets(self):
        model = self.view_assets.model()
        if not model:
            return
        model.clear_assets()

    @Slot()
    def reload(self):
        model = self.view_assets.model()
        if not model:
            return
        model.clear_assets()
        path = model.assets_folder
        if path:
            self.assets_folder.emit(path)

    @Slot(str, int)
    def handle_announcement(self, job_name, job_size):
        self.setWindowTitle("序列上傳 [{}]".format(job_name))
        self.bar_progress.setMinimum(0)
        self.bar_progress.setMaximum(job_size)

    @Slot(int)
    def handle_progress(self, new_progress):
        self.bar_progress.setValue(new_progress)

    @Slot(int)
    def handle_progress1(self, json_path, new_progress):
        """暫時性命名，準備取代原來的, handle_progress"""
        self._model.set_progressbar(json_path, new_progress)

    @Slot()
    def handle_complete(self):
        self.setWindowTitle("序列上傳")
        self.bar_progress.reset()

    @Slot()
    def toggle_busy(self, stat=None):
        if stat is None:
            self._busy = not self._busy
        else:
            self._busy = bool(stat)
        if self._busy:
            self.setCursor(Qt.CursorShape.BusyCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    @Slot()
    def _view_assets_gen_thumbnail(self, idx:QModelIndex):
        model = idx.model()
        if not model:
            return

        data = model.data(idx, AssetRole)
        thumb_source = os.path.join(data["preview_folder"], "Large_0.jpg")
        if not os.path.exists(thumb_source):
            msg = QMessageBox(self, "Wraning", "Find No Large_0.jpg")
            msg.setWindowModality(Qt.WindowModality.WindowModal)
            msg.show()

        self.gen_thumbnail.emit(data["json_path"], thumb_source)
        return True

    def set_preview(self, key, icon_file):
        if not self._model:
            return
        self._model.set_preview(key, icon_file)

    def updateColumnSize(self):
        horizontalHeader = self.view_assets.horizontalHeader()
        for i in range(self._model.columnCount()):
            horizontalHeader.setSectionResizeMode(i, horizontalHeader.ResizeMode.ResizeToContents)
