import os
from PySide6.QtCore import Qt, Signal, QItemSelection, QItemSelectionModel, QModelIndex
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import QTableView, QMenu
from . import ProgressDelegate, UploadModel


class AssetsTableView(QTableView):
    gen_thumbnail = Signal(object)

    def __init__(self, parent=None):
        super(AssetsTableView, self).__init__(parent)
        self.__progress_delegate = ProgressDelegate()
        self.setItemDelegateForColumn(1, self.__progress_delegate)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        invert_act: QAction = menu.addAction(self.tr("&Invert Selection"))
        invert_act.setShortcut(QKeySequence("Ctrl+I"))
        toggle_act: QAction = menu.addAction(self.tr("&Toggle Selection"))
        toggle_act.setShortcut(QKeySequence("Ctrl+T"))
        copy2eng_act: QAction = menu.addAction(
            self.tr("&Copy Filename To English Name")
        )
        copy2eng_act.setShortcut(QKeySequence("Ctrl+E"))
        gen_thumbnail_act: QAction = menu.addAction(
            self.tr("&Create Thumbnail From Preview")
        )
        gen_thumbnail_act.setShortcut(QKeySequence("Ctrl+P"))

        action = menu.exec_(self.mapToGlobal(event.pos()))
        model = self.model()
        if not model:
            return

        if action == invert_act:
            return self._invert_selection()
        if action == toggle_act:
            return self._toggle_selection()
        if action == copy2eng_act:
            return self._copy2eng_act()
        if action == gen_thumbnail_act:
            return self._gen_thumbnail_act()

    def _invert_selection(self):
        sel_model = self.selectionModel()
        rows = self.model().rowCount()
        columns = self.model().columnCount()
        topLeft = self.model().createIndex(0, 0)
        bottomRignt = self.model().createIndex(rows - 1, columns - 1)
        all_sel = QItemSelection(topLeft, bottomRignt)
        sel_model.select(all_sel, QItemSelectionModel.SelectionFlag.Toggle)

    def _toggle_selection(self):
        sel_model = self.selectionModel()
        selection = sel_model.selectedRows()

        if all(map(self.__get_check_stat, selection)):
            self.__set_check_stat(selection, Qt.CheckState.Unchecked)
        else:
            self.__set_check_stat(selection, Qt.CheckState.Checked)

    def _copy2eng_act(self):
        sel_model = self.selectionModel()
        selection = sel_model.selectedRows()
        for idx in selection:
            self.__copy2eng(idx)

    def _gen_thumbnail_act(self):
        sel_model = self.selectionModel()
        selection = sel_model.selectedRows()
        for idx in selection:
            self.__gen_thumbnail(idx)

    def __get_check_stat(self, idx):
        model = self.model()
        qt_checked = model.data(idx, Qt.ItemDataRole.CheckStateRole)
        checked = True if qt_checked == Qt.CheckState.Checked else False
        return checked

    def __set_check_stat(self, selection, val):
        model = self.model()
        for idx in selection:
            model.setData(idx, val)

    def __copy2eng(self, idx: QModelIndex):
        assetpath_key = "asset_path"
        assetpath_col_idx = -1
        cols = self.model().columnCount()
        for i in range(cols):
            header_key = self.model().headerData(i, Qt.Orientation.Horizontal)
            if header_key == assetpath_key:
                assetpath_col_idx = i
            if assetpath_col_idx != -1:
                break
        if assetpath_col_idx == -1:
            return
        # 找出 asset path 在哪個 column

        assetpath_idx = self.model().createIndex(idx.row(), assetpath_col_idx)
        assetpath = self.model().data(assetpath_idx)
        asset_name = os.path.basename(assetpath)
        asset_name = asset_name.split(".")[0]
        eng_idx = self.model().createIndex(
            idx.row(), 4
        )  # english name 的欄位是寫死在這裡的喔。請小心 (4)
        self.model().setData(eng_idx, asset_name)

    def __gen_thumbnail(self, idx: QModelIndex):
        if not idx.isValid():
            return
        self.gen_thumbnail.emit(idx)

    def model(self) -> "UploadModel":
        return super(AssetsTableView, self).model()