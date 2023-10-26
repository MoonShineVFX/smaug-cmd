# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from smaug_cmd.ui import (AssetEditorWidget, EmptyWidget)

class Ui_asset_widget(object):
    def setupUi(self, asset_widget):
        if not asset_widget.objectName():
            asset_widget.setObjectName(u"asset_widget")
        asset_widget.resize(420, 766)
        self.asset_page = AssetEditorWidget()
        self.asset_page.setObjectName(u"asset_page")
        self.verticalLayout = QVBoxLayout(self.asset_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        asset_widget.addWidget(self.asset_page)
        self.empty_page = EmptyWidget()
        self.empty_page.setObjectName(u"empty_page")
        self.verticalLayout_2 = QVBoxLayout(self.empty_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        asset_widget.addWidget(self.empty_page)

        self.retranslateUi(asset_widget)

        asset_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(asset_widget)
    # setupUi

    def retranslateUi(self, asset_widget):
        asset_widget.setWindowTitle(QCoreApplication.translate("asset_widget", u"StackedWidget", None))
    # retranslateUi

