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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from smaug_cmd.ui import MoonFrame

class Ui_base_frome(object):
    def setupUi(self, base_frome):
        if not base_frome.objectName():
            base_frome.setObjectName(u"base_frome")
        base_frome.resize(418, 806)
        self.verticalLayout = QVBoxLayout(base_frome)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.asset_frame = MoonFrame(base_frome)
        self.asset_frame.setObjectName(u"asset_frame")
        self.asset_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.asset_frame)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.asset_into_frame = MoonFrame(self.asset_frame)
        self.asset_into_frame.setObjectName(u"asset_into_frame")
        self.asset_into_frame.setFrameShape(QFrame.StyledPanel)
        self.asset_into_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.asset_into_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 0, 0, 0)
        self.asset_name_lbl = QLabel(self.asset_into_frame)
        self.asset_name_lbl.setObjectName(u"asset_name_lbl")
        font = QFont()
        font.setPointSize(24)
        self.asset_name_lbl.setFont(font)
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


        self.retranslateUi(base_frome)

        QMetaObject.connectSlotsByName(base_frome)
    # setupUi

    def retranslateUi(self, base_frome):
        base_frome.setWindowTitle(QCoreApplication.translate("base_frome", u"Form", None))
        self.asset_name_lbl.setText(QCoreApplication.translate("base_frome", u"Asset Name", None))
        self.asset_id_lbl.setText(QCoreApplication.translate("base_frome", u"Id: None", None))
        self.asset_cate_lbl.setText(QCoreApplication.translate("base_frome", u"category: None  ", None))
        self.catePicker_btn.setText(QCoreApplication.translate("base_frome", u"...", None))
    # retranslateUi

