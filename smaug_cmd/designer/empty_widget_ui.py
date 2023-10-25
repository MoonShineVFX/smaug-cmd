# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'empty_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import smaug_rc

class Ui_empty_frame(object):
    def setupUi(self, empty_frame):
        if not empty_frame.objectName():
            empty_frame.setObjectName(u"empty_frame")
        empty_frame.resize(420, 567)
        empty_frame.setMaximumSize(QSize(420, 16777215))
        self.verticalLayout = QVBoxLayout(empty_frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.empty_pic_frame = QFrame(empty_frame)
        self.empty_pic_frame.setObjectName(u"empty_pic_frame")
        self.empty_pic_frame.setMinimumSize(QSize(0, 200))
        self.empty_pic_frame.setMaximumSize(QSize(16777215, 200))
        self.empty_pic_frame.setStyleSheet(u"#empty_pic_frame{\n"
"    background-image: url(:/ui/empty.png);\n"
"    background-position: center center;\n"
"    background-repeat: no-repeat;\n"
"}")
        self.empty_pic_frame.setFrameShape(QFrame.StyledPanel)
        self.empty_pic_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.empty_pic_frame)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(empty_frame)

        QMetaObject.connectSlotsByName(empty_frame)
    # setupUi

    def retranslateUi(self, empty_frame):
        empty_frame.setWindowTitle(QCoreApplication.translate("empty_frame", u"Form", None))
    # retranslateUi

