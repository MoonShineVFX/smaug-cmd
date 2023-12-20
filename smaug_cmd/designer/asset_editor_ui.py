# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from smaug_cmd.ui import (FileListWidget, ImageDisplayWidget, MoonFrame, TagsWidget)
import smaug_cmd_rc

class Ui_asset_editor_wgt(object):
    def setupUi(self, asset_editor_wgt):
        if not asset_editor_wgt.objectName():
            asset_editor_wgt.setObjectName(u"asset_editor_wgt")
        asset_editor_wgt.resize(480, 917)
        asset_editor_wgt.setMaximumSize(QSize(480, 16777215))
        asset_editor_wgt.setStyleSheet(u"#asset_name_lbl, #asset_id_lbl, #asset_cate_lbl{\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#asset_into_frame {\n"
"    background-image: url(:/ui/no_preview.png);\n"
"    background-color: rgba(0, 0, 0, 0.5);\n"
"    background-position: center center;\n"
"    background-repeat: no-repeat;\n"
"}")
        self.verticalLayout = QVBoxLayout(asset_editor_wgt)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.asset_frame = QWidget(asset_editor_wgt)
        self.asset_frame.setObjectName(u"asset_frame")
        self.verticalLayout_5 = QVBoxLayout(self.asset_frame)
        self.verticalLayout_5.setSpacing(12)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.asset_info_frame = MoonFrame(self.asset_frame)
        self.asset_info_frame.setObjectName(u"asset_info_frame")
        self.asset_info_frame.setMinimumSize(QSize(0, 270))
        self.asset_info_frame.setMaximumSize(QSize(16777215, 270))
        self.asset_info_frame.setStyleSheet(u"")
        self.asset_info_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_info_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.asset_info_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.asset_name_lbl = QLabel(self.asset_info_frame)
        self.asset_name_lbl.setObjectName(u"asset_name_lbl")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.asset_name_lbl.setFont(font)
        self.asset_name_lbl.setStyleSheet(u"")
        self.asset_name_lbl.setMargin(0)

        self.verticalLayout_3.addWidget(self.asset_name_lbl)

        self.verticalSpacer = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.asset_id_lbl = QLabel(self.asset_info_frame)
        self.asset_id_lbl.setObjectName(u"asset_id_lbl")
        self.asset_id_lbl.setMargin(0)

        self.verticalLayout_3.addWidget(self.asset_id_lbl)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.asset_cate_lbl = QLabel(self.asset_info_frame)
        self.asset_cate_lbl.setObjectName(u"asset_cate_lbl")

        self.horizontalLayout_3.addWidget(self.asset_cate_lbl)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.cate_picker_btn = QPushButton(self.asset_info_frame)
        self.cate_picker_btn.setObjectName(u"cate_picker_btn")
        self.cate_picker_btn.setMaximumSize(QSize(24, 20))
        self.cate_picker_btn.setStyleSheet(u"QPushButton#catePicker_btn[smaug_cate=\"false\"]{\n"
"background-color: rgb(170, 0, 0);\n"
"}\n"
"QPushButton#catePicker_btn[smaug_cate=\"true\"]{\n"
"background-color: rgb(0, 109, 18);\n"
"}")
        self.cate_picker_btn.setFlat(False)
        self.cate_picker_btn.setProperty("smaug_cate", False)

        self.horizontalLayout_3.addWidget(self.cate_picker_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_5.addWidget(self.asset_info_frame)

        self.tag_frame = MoonFrame(self.asset_frame)
        self.tag_frame.setObjectName(u"tag_frame")
        self.tag_frame.setFrameShape(QFrame.StyledPanel)
        self.tag_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.tag_frame)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.tags_grp = QGroupBox(self.tag_frame)
        self.tags_grp.setObjectName(u"tags_grp")
        self.verticalLayout_9 = QVBoxLayout(self.tags_grp)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.tags_widget = TagsWidget(self.tags_grp)
        self.tags_widget.setObjectName(u"tags_widget")
        self.tags_widget.setMinimumSize(QSize(0, 100))
        self.tags_widget.setBaseSize(QSize(0, 0))

        self.verticalLayout_9.addWidget(self.tags_widget)


        self.verticalLayout_10.addWidget(self.tags_grp)


        self.verticalLayout_5.addWidget(self.tag_frame)


        self.verticalLayout.addWidget(self.asset_frame)

        self.scrollArea = QScrollArea(asset_editor_wgt)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 461, 656))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.preview_grp = QGroupBox(self.scrollAreaWidgetContents)
        self.preview_grp.setObjectName(u"preview_grp")
        self.preview_grp.setMinimumSize(QSize(0, 0))
        self.preview_grp.setCheckable(False)
        self.verticalLayout_4 = QVBoxLayout(self.preview_grp)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.preview_widget = ImageDisplayWidget(self.preview_grp)
        self.preview_widget.setObjectName(u"preview_widget")
        self.preview_widget.setMinimumSize(QSize(0, 120))
        self.preview_widget.setMaximumSize(QSize(16777215, 180))
        font1 = QFont()
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.preview_widget.setFont(font1)

        self.verticalLayout_4.addWidget(self.preview_widget)


        self.verticalLayout_2.addWidget(self.preview_grp)

        self.model_files_grp = QGroupBox(self.scrollAreaWidgetContents)
        self.model_files_grp.setObjectName(u"model_files_grp")
        self.verticalLayout_6 = QVBoxLayout(self.model_files_grp)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.model_widget = FileListWidget(self.model_files_grp)
        self.model_widget.setObjectName(u"model_widget")
        self.model_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_6.addWidget(self.model_widget)


        self.verticalLayout_2.addWidget(self.model_files_grp)

        self.texture_grp = QGroupBox(self.scrollAreaWidgetContents)
        self.texture_grp.setObjectName(u"texture_grp")
        self.verticalLayout_8 = QVBoxLayout(self.texture_grp)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textures_widget = FileListWidget(self.texture_grp)
        self.textures_widget.setObjectName(u"textures_widget")
        self.textures_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_8.addWidget(self.textures_widget)


        self.verticalLayout_2.addWidget(self.texture_grp)

        self.render_grp = QGroupBox(self.scrollAreaWidgetContents)
        self.render_grp.setObjectName(u"render_grp")
        self.verticalLayout_7 = QVBoxLayout(self.render_grp)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.render_widget = ImageDisplayWidget(self.render_grp)
        self.render_widget.setObjectName(u"render_widget")
        self.render_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_7.addWidget(self.render_widget)


        self.verticalLayout_2.addWidget(self.render_grp)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalLayout.setStretch(1, 1)
        QWidget.setTabOrder(self.cate_picker_btn, self.scrollArea)

        self.retranslateUi(asset_editor_wgt)

        QMetaObject.connectSlotsByName(asset_editor_wgt)
    # setupUi

    def retranslateUi(self, asset_editor_wgt):
        asset_editor_wgt.setWindowTitle(QCoreApplication.translate("asset_editor_wgt", u"Form", None))
        self.asset_name_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Asset Name", None))
        self.asset_id_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Id: None", None))
        self.asset_cate_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Category: None  ", None))
        self.cate_picker_btn.setText(QCoreApplication.translate("asset_editor_wgt", u"...", None))
        self.tags_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Tags Editor", None))
        self.preview_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Preview Picture", None))
        self.model_files_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Model Files", None))
        self.texture_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Texture Files", None))
        self.render_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Render Pictures", None))
    # retranslateUi

