# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from smaug_cmd.ui import (FileListWidget, ImageDisplayWidget, MoonFrame, TagsWidget)

class Ui_asset_editor_wgt(object):
    def setupUi(self, asset_editor_wgt):
        if not asset_editor_wgt.objectName():
            asset_editor_wgt.setObjectName(u"asset_editor_wgt")
        asset_editor_wgt.resize(434, 1132)
        asset_editor_wgt.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(asset_editor_wgt)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.asset_frame = MoonFrame(asset_editor_wgt)
        self.asset_frame.setObjectName(u"asset_frame")
        self.asset_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.asset_frame)
        self.verticalLayout_5.setSpacing(12)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.asset_into_frame = MoonFrame(self.asset_frame)
        self.asset_into_frame.setObjectName(u"asset_into_frame")
        self.asset_into_frame.setMaximumSize(QSize(16777215, 16777215))
        self.asset_into_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_into_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.asset_into_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.asset_info_grp = QGroupBox(self.asset_into_frame)
        self.asset_info_grp.setObjectName(u"asset_info_grp")
        self.asset_info_grp.setEnabled(True)
        self.asset_info_grp.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        self.asset_info_grp.setFont(font)
        self.asset_info_grp.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.asset_info_grp)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.asset_name_lbl = QLabel(self.asset_info_grp)
        self.asset_name_lbl.setObjectName(u"asset_name_lbl")
        font1 = QFont()
        font1.setPointSize(24)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        self.asset_name_lbl.setFont(font1)
        self.asset_name_lbl.setMargin(0)

        self.verticalLayout_2.addWidget(self.asset_name_lbl)

        self.verticalSpacer = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.asset_id_lbl = QLabel(self.asset_info_grp)
        self.asset_id_lbl.setObjectName(u"asset_id_lbl")
        self.asset_id_lbl.setMargin(0)

        self.verticalLayout_2.addWidget(self.asset_id_lbl)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.asset_cate_lbl = QLabel(self.asset_info_grp)
        self.asset_cate_lbl.setObjectName(u"asset_cate_lbl")

        self.horizontalLayout_3.addWidget(self.asset_cate_lbl)

        self.cate_picker_btn = QPushButton(self.asset_info_grp)
        self.cate_picker_btn.setObjectName(u"cate_picker_btn")
        self.cate_picker_btn.setMaximumSize(QSize(24, 20))
        self.cate_picker_btn.setStyleSheet(u"QPushButton#catePicker_btn[smaug_cate=\"false\"]{\n"
"background-color: rgb(170, 0, 0);\n"
"}\n"
"QPushButton#catePicker_btn[smaug_cate=\"true\"]{\n"
"background-color: rgb(0, 109, 18);\n"
"}")
        self.cate_picker_btn.setProperty("smaug_cate", False)

        self.horizontalLayout_3.addWidget(self.cate_picker_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.asset_info_grp)


        self.verticalLayout_5.addWidget(self.asset_into_frame)

        self.preview_grp = QGroupBox(self.asset_frame)
        self.preview_grp.setObjectName(u"preview_grp")
        self.preview_grp.setMinimumSize(QSize(0, 260))
        self.preview_grp.setCheckable(False)
        self.verticalLayout_4 = QVBoxLayout(self.preview_grp)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.preview_widget = ImageDisplayWidget(self.preview_grp)
        self.preview_widget.setObjectName(u"preview_widget")
        self.preview_widget.setMinimumSize(QSize(0, 220))
        self.preview_widget.setMaximumSize(QSize(16777215, 220))
        font2 = QFont()
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.preview_widget.setFont(font2)

        self.verticalLayout_4.addWidget(self.preview_widget)


        self.verticalLayout_5.addWidget(self.preview_grp)

        self.model_files_grp = QGroupBox(self.asset_frame)
        self.model_files_grp.setObjectName(u"model_files_grp")
        self.verticalLayout_6 = QVBoxLayout(self.model_files_grp)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.model_widget = FileListWidget(self.model_files_grp)
        self.model_widget.setObjectName(u"model_widget")
        self.model_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_6.addWidget(self.model_widget)


        self.verticalLayout_5.addWidget(self.model_files_grp)

        self.render_grp = QGroupBox(self.asset_frame)
        self.render_grp.setObjectName(u"render_grp")
        self.verticalLayout_7 = QVBoxLayout(self.render_grp)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.render_widget = ImageDisplayWidget(self.render_grp)
        self.render_widget.setObjectName(u"render_widget")
        self.render_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_7.addWidget(self.render_widget)


        self.verticalLayout_5.addWidget(self.render_grp)

        self.texture_grp = QGroupBox(self.asset_frame)
        self.texture_grp.setObjectName(u"texture_grp")
        self.verticalLayout_8 = QVBoxLayout(self.texture_grp)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textures_widget = FileListWidget(self.texture_grp)
        self.textures_widget.setObjectName(u"textures_widget")
        self.textures_widget.setMinimumSize(QSize(0, 120))

        self.verticalLayout_8.addWidget(self.textures_widget)


        self.verticalLayout_5.addWidget(self.texture_grp)

        self.tags_grp = QGroupBox(self.asset_frame)
        self.tags_grp.setObjectName(u"tags_grp")
        self.verticalLayout_9 = QVBoxLayout(self.tags_grp)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 6, 0, -1)
        self.tags_widget = TagsWidget(self.tags_grp)
        self.tags_widget.setObjectName(u"tags_widget")
        self.tags_widget.setMinimumSize(QSize(0, 100))
        self.tags_widget.setBaseSize(QSize(0, 0))

        self.verticalLayout_9.addWidget(self.tags_widget)


        self.verticalLayout_5.addWidget(self.tags_grp)


        self.verticalLayout.addWidget(self.asset_frame)


        self.retranslateUi(asset_editor_wgt)

        QMetaObject.connectSlotsByName(asset_editor_wgt)
    # setupUi

    def retranslateUi(self, asset_editor_wgt):
        asset_editor_wgt.setWindowTitle(QCoreApplication.translate("asset_editor_wgt", u"Form", None))
        self.asset_info_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Asset Info", None))
        self.asset_name_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Asset Name", None))
        self.asset_id_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Id: None", None))
        self.asset_cate_lbl.setText(QCoreApplication.translate("asset_editor_wgt", u"Category: None  ", None))
        self.cate_picker_btn.setText(QCoreApplication.translate("asset_editor_wgt", u"...", None))
        self.preview_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Preview Picture", None))
        self.model_files_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Model Files", None))
        self.render_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Render Pictures", None))
        self.texture_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Texture Files", None))
        self.tags_grp.setTitle(QCoreApplication.translate("asset_editor_wgt", u"Tags Editor", None))
    # retranslateUi

