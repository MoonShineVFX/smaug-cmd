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
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_asset_list_dlg(object):
    def setupUi(self, asset_list_dlg):
        if not asset_list_dlg.objectName():
            asset_list_dlg.setObjectName(u"asset_list_dlg")
        asset_list_dlg.resize(704, 871)
        self.horizontalLayout = QHBoxLayout(asset_list_dlg)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.folder_tree_frame = QFrame(asset_list_dlg)
        self.folder_tree_frame.setObjectName(u"folder_tree_frame")
        self.folder_tree_frame.setMinimumSize(QSize(200, 0))
        self.folder_tree_frame.setFrameShape(QFrame.StyledPanel)
        self.folder_tree_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.folder_tree_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.folder_tree_widget = QWidget(self.folder_tree_frame)
        self.folder_tree_widget.setObjectName(u"folder_tree_widget")

        self.verticalLayout_2.addWidget(self.folder_tree_widget)


        self.horizontalLayout.addWidget(self.folder_tree_frame)

        self.item_frame = QFrame(asset_list_dlg)
        self.item_frame.setObjectName(u"item_frame")
        self.item_frame.setMinimumSize(QSize(480, 0))
        self.item_frame.setFrameShape(QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.item_frame)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 0, 0, 0)
        self.function_button_frame = QFrame(self.item_frame)
        self.function_button_frame.setObjectName(u"function_button_frame")
        self.function_button_frame.setFrameShape(QFrame.StyledPanel)
        self.function_button_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.function_button_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, -1)
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

        self.uploader_pgbar = QProgressBar(self.function_button_frame)
        self.uploader_pgbar.setObjectName(u"uploader_pgbar")
        self.uploader_pgbar.setMaximumSize(QSize(16777215, 6))
        font = QFont()
        font.setKerning(True)
        self.uploader_pgbar.setFont(font)
        self.uploader_pgbar.setValue(24)
        self.uploader_pgbar.setTextVisible(False)

        self.verticalLayout_4.addWidget(self.uploader_pgbar)


        self.verticalLayout.addWidget(self.function_button_frame)

        self.asset_frame = QFrame(self.item_frame)
        self.asset_frame.setObjectName(u"asset_frame")
        self.asset_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.asset_frame)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.asset_into_frame = QFrame(self.asset_frame)
        self.asset_into_frame.setObjectName(u"asset_into_frame")
        self.asset_into_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_into_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.asset_into_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 0, 0, 0)
        self.asset_name_lbl = QLabel(self.asset_into_frame)
        self.asset_name_lbl.setObjectName(u"asset_name_lbl")
        font1 = QFont()
        font1.setPointSize(24)
        self.asset_name_lbl.setFont(font1)
        self.asset_name_lbl.setMargin(0)

        self.verticalLayout_3.addWidget(self.asset_name_lbl)

        self.verticalSpacer = QSpacerItem(20, 6, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.asset_id_lbl = QLabel(self.asset_into_frame)
        self.asset_id_lbl.setObjectName(u"asset_id_lbl")
        self.asset_id_lbl.setMargin(0)

        self.verticalLayout_3.addWidget(self.asset_id_lbl)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.asset_cate_lbl = QLabel(self.asset_into_frame)
        self.asset_cate_lbl.setObjectName(u"asset_cate_lbl")

        self.horizontalLayout_3.addWidget(self.asset_cate_lbl)

        self.catePicker_btn = QPushButton(self.asset_into_frame)
        self.catePicker_btn.setObjectName(u"catePicker_btn")
        self.catePicker_btn.setMaximumSize(QSize(24, 20))
        self.catePicker_btn.setStyleSheet(u"QPushButton#catePicker_btn[smaug_cate=\"false\"]{\n"
"background-color: rgb(170, 0, 0);\n"
"}\n"
"QPushButton#catePicker_btn[smaug_cate=\"true\"]{\n"
"background-color: rgb(0, 109, 18);\n"
"}")
        self.catePicker_btn.setProperty("smaug_cate", False)

        self.horizontalLayout_3.addWidget(self.catePicker_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_5.addWidget(self.asset_into_frame)

        self.preview_widget = QWidget(self.asset_frame)
        self.preview_widget.setObjectName(u"preview_widget")
        self.preview_widget.setMinimumSize(QSize(0, 220))
        self.preview_widget.setMaximumSize(QSize(16777215, 220))

        self.verticalLayout_5.addWidget(self.preview_widget)

        self.model_widget = QWidget(self.asset_frame)
        self.model_widget.setObjectName(u"model_widget")
        self.model_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_5.addWidget(self.model_widget)

        self.textures_widget = QWidget(self.asset_frame)
        self.textures_widget.setObjectName(u"textures_widget")
        self.textures_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_5.addWidget(self.textures_widget)

        self.render_widget = QWidget(self.asset_frame)
        self.render_widget.setObjectName(u"render_widget")
        self.render_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_5.addWidget(self.render_widget)

        self.tags_widget = QWidget(self.asset_frame)
        self.tags_widget.setObjectName(u"tags_widget")
        self.tags_widget.setMinimumSize(QSize(0, 100))
        self.tags_widget.setBaseSize(QSize(0, 0))

        self.verticalLayout_5.addWidget(self.tags_widget)

        self.verticalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.setStretch(3, 1)
        self.verticalLayout_5.setStretch(5, 1)

        self.verticalLayout.addWidget(self.asset_frame)

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
        self.asset_name_lbl.setText(QCoreApplication.translate("asset_list_dlg", u"Asset Name", None))
        self.asset_id_lbl.setText(QCoreApplication.translate("asset_list_dlg", u"Id: None", None))
        self.asset_cate_lbl.setText(QCoreApplication.translate("asset_list_dlg", u"category: None  ", None))
        self.catePicker_btn.setText(QCoreApplication.translate("asset_list_dlg", u"...", None))
    # retranslateUi

