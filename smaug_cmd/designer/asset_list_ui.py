# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_list.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

from smaug_cmd.ui import (AssetWidget, FolderSelector, FolderTreeWidget, MoonFrame)
import smaug_cmd_rc

class Ui_asset_list_dlg(object):
    def setupUi(self, asset_list_dlg):
        if not asset_list_dlg.objectName():
            asset_list_dlg.setObjectName(u"asset_list_dlg")
        asset_list_dlg.resize(704, 859)
        self.horizontalLayout = QHBoxLayout(asset_list_dlg)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.folder_tree_frame = MoonFrame(asset_list_dlg)
        self.folder_tree_frame.setObjectName(u"folder_tree_frame")
        self.folder_tree_frame.setMinimumSize(QSize(200, 0))
        self.folder_tree_frame.setFrameShape(QFrame.StyledPanel)
        self.folder_tree_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.folder_tree_frame)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.folder_picker_widget = FolderSelector(self.folder_tree_frame)
        self.folder_picker_widget.setObjectName(u"folder_picker_widget")
        self.folder_picker_widget.setMinimumSize(QSize(0, 32))

        self.verticalLayout_2.addWidget(self.folder_picker_widget)

        self.folder_tree_widget = FolderTreeWidget(self.folder_tree_frame)
        self.folder_tree_widget.setObjectName(u"folder_tree_widget")

        self.verticalLayout_2.addWidget(self.folder_tree_widget)

        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.folder_tree_frame)

        self.item_frame = MoonFrame(asset_list_dlg)
        self.item_frame.setObjectName(u"item_frame")
        self.item_frame.setMinimumSize(QSize(480, 0))
        self.item_frame.setFrameShape(QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.item_frame)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 0, 0, 0)
        self.function_button_frame = MoonFrame(self.item_frame)
        self.function_button_frame.setObjectName(u"function_button_frame")
        self.function_button_frame.setFrameShape(QFrame.StyledPanel)
        self.function_button_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.function_button_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.push_db_btn = QPushButton(self.function_button_frame)
        self.push_db_btn.setObjectName(u"push_db_btn")
        self.push_db_btn.setMinimumSize(QSize(0, 32))
        self.push_db_btn.setStyleSheet(u"QPushButton#push_db_btn[has_id=\"false\"]{\n"
"	background-color: rgb(0, 109, 18);\n"
"}")
        self.push_db_btn.setProperty("has_id", False)

        self.horizontalLayout_2.addWidget(self.push_db_btn)

        self.delete_btn = QPushButton(self.function_button_frame)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(0, 32))

        self.horizontalLayout_2.addWidget(self.delete_btn)

        self.update_btn = QPushButton(self.function_button_frame)
        self.update_btn.setObjectName(u"update_btn")
        self.update_btn.setMinimumSize(QSize(0, 32))
        self.update_btn.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_2.addWidget(self.update_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.function_button_frame)

        self.scrollArea = QScrollArea(self.item_frame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 470, 795))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.asset_widget = AssetWidget(self.scrollAreaWidgetContents)
        self.asset_widget.setObjectName(u"asset_widget")

        self.verticalLayout_3.addWidget(self.asset_widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.item_frame)


        self.retranslateUi(asset_list_dlg)

        QMetaObject.connectSlotsByName(asset_list_dlg)
    # setupUi

    def retranslateUi(self, asset_list_dlg):
        asset_list_dlg.setWindowTitle(QCoreApplication.translate("asset_list_dlg", u"Dialog", None))
        self.push_db_btn.setText(QCoreApplication.translate("asset_list_dlg", u"Push to DB", None))
        self.delete_btn.setText(QCoreApplication.translate("asset_list_dlg", u"Update", None))
        self.update_btn.setText(QCoreApplication.translate("asset_list_dlg", u"Delete", None))
    # retranslateUi

