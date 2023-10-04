import logging
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QFileSystemModel
from PySide6.QtCore import QDir, QModelIndex, Signal, QSortFilterProxyModel

logger = logging.getLogger("smaug.ui")


class DirOnlyProxyModel(QSortFilterProxyModel):
    def hasChildren(self, index: QModelIndex) -> bool:
        source_index = self.mapToSource(index)
        if self.sourceModel().isDir(source_index):
            dir_path = self.sourceModel().filePath(source_index)
            dir_entry = QDir(dir_path).entryList(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
            # Count the number of directories inside this directory
            return len(dir_entry) > 0
        return False


class FolderTreeWidget(QWidget):
    selectedFolder = Signal(str)

    def __init__(self, parent=None):
        super(FolderTreeWidget, self).__init__(parent)  

        self.setWindowTitle("Directory Tree Browser")
        # self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # File System Model
        self.model = QFileSystemModel()
        self.proxy_model = DirOnlyProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.model.setRootPath(QDir.homePath())
        self.model.setFilter(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)

        # Tree View
        self.tree = QTreeView()
        self.tree.setModel(self.proxy_model)
        proxy_root_index = self.proxy_model.mapFromSource(self.model.index(QDir.homePath()))
        self.tree.setRootIndex(proxy_root_index)
        self.tree.setColumnWidth(0, 250)

        # Adding TreeView to layout
        layout.addWidget(self.tree)

        self.tree.clicked.connect(self._on_treeView_clicked)

    def _on_treeView_clicked(self, index: QModelIndex):
        path = self._get_current_directory(index)
        logger.debug(path)
        self.selectedFolder.emit(path)

    def currentSelectedPath(self):
        return self._get_current_directory()

    def _get_current_directory(self, proxy_index: QModelIndex):
        # 獲取當前選定的索引
        source_index = self.proxy_model.mapToSource(proxy_index)
        # 使用模型將索引轉換為路徑
        path = self.model.filePath(source_index)
        return path
