# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import QDialog, QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from smaug_cmd.ui import FolderTreeWidget


class Ui_asset_list_dialog(object):
    def setupUi(self, asset_list_dialog: QDialog):
        if not asset_list_dialog.objectName():
            asset_list_dialog.setObjectName("asset_list_dialog")
        asset_list_dialog.resize(704, 823)
        self.horizontalLayout = QHBoxLayout(asset_list_dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.folder_tree_frame = QFrame(asset_list_dialog)
        self.folder_tree_frame.setObjectName("folder_tree_frame")
        self.folder_tree_frame.setMinimumSize(QSize(300, 0))
        self.folder_tree_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.folder_tree_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.folder_tree_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.folder_tree_widget = FolderTreeWidget(self.folder_tree_frame)
        self.folder_tree_widget.setObjectName("folder_tree_widget")
        self.verticalLayout_3.addWidget(self.folder_tree_widget)

        self.horizontalLayout.addWidget(self.folder_tree_frame)

        self.asset_property_frame = QFrame(asset_list_dialog)
        self.asset_property_frame.setObjectName("asset_property_frame")
        self.asset_property_frame.setMinimumSize(QSize(480, 0))
        self.asset_property_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.asset_property_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.asset_property_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(9, 0, 9, 0)
        self.function_button_frame = QFrame(self.asset_property_frame)
        self.function_button_frame.setObjectName("function_button_frame")
        self.function_button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.function_button_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.function_button_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Create_btn = QPushButton(self.function_button_frame)
        self.Create_btn.setObjectName("Create_btn")

        self.horizontalLayout_2.addWidget(self.Create_btn)

        self.delete_btn = QPushButton(self.function_button_frame)
        self.delete_btn.setObjectName("delete_btn")

        self.horizontalLayout_2.addWidget(self.delete_btn)

        self.update_btn = QPushButton(self.function_button_frame)
        self.update_btn.setObjectName("update_btn")
        self.update_btn.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_2.addWidget(self.update_btn)

        self.verticalLayout.addWidget(self.function_button_frame)

        self.preview_frame = QFrame(self.asset_property_frame)
        self.preview_frame.setObjectName("preview_frame")
        self.preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preview_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.preview_frame)

        self.model_frame = QFrame(self.asset_property_frame)
        self.model_frame.setObjectName("model_frame")
        self.model_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.model_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.model_frame)

        self.render_frame = QFrame(self.asset_property_frame)
        self.render_frame.setObjectName("render_frame")
        self.render_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.render_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.render_frame)

        self.texture_frame = QFrame(self.asset_property_frame)
        self.texture_frame.setObjectName("texture_frame")
        self.texture_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.texture_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.texture_frame)

        self.tags_frame = QFrame(self.asset_property_frame)
        self.tags_frame.setObjectName("tags_frame")
        self.tags_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.tags_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.tags_frame)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.horizontalLayout.addWidget(self.asset_property_frame)

        self.retranslateUi(asset_list_dialog)

        QMetaObject.connectSlotsByName(asset_list_dialog)

    # setupUi

    def retranslateUi(self, asset_list_dialog: QDialog):
        asset_list_dialog.setWindowTitle(
            QCoreApplication.translate("asset_list_dialog", "Dialog", None)
        )
        self.Create_btn.setText(
            QCoreApplication.translate("asset_list_dialog", "Create", None)
        )
        self.delete_btn.setText(
            QCoreApplication.translate("asset_list_dialog", "Update", None)
        )
        self.update_btn.setText(
            QCoreApplication.translate("asset_list_dialog", "Delete", None)
        )

    # retranslateUi


class AssetListDialog(QDialog, Ui_asset_list_dialog):
    def __init__(self, parent=None):
        super(AssetListDialog, self).__init__(parent)
        self.setupUi(self)


class EmptyWidget(QWidget):
    def __init__(self, parent=None):
        super(EmptyWidget, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget()
        pixmap = QPixmap(path).scaledToHeight(180)
        label = QLabel(self.scrollAreaWidgetContents)
        label.setPixmap(pixmap)
        self.horizontalLayout.addWidget(label)


