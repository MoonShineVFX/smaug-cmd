# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import QDialog, QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from smaug_cmd.ui import FolderTreeWidget
from smaug_cmd.designer.asset_list_ui import Ui_asset_list_dlg


class AssetListDialog(QDialog, Ui_asset_list_dlg):
    def __init__(self, parent=None):
        super(AssetListDialog, self).__init__(parent)
        self.setupUi(self)


# class EmptyWidget(QWidget):
#     def __init__(self, parent=None):
#         super(EmptyWidget, self).__init__(parent)
#         lay = QVBoxLayout(self)
#         lay.addWidget()
#         pixmap = QPixmap(path).scaledToHeight(180)
#         label = QLabel(self.scrollAreaWidgetContents)
#         label.setPixmap(pixmap)
#         self.horizontalLayout.addWidget(label)


