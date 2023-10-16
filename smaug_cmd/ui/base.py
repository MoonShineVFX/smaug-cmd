# import sys

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap

class MoonFrame(QFrame):
    def __init__(self, parent=None):
        super(MoonFrame, self).__init__(parent)
        # if sys.platform == "win32":
        self.setStyleSheet("MoonFrame{border: 0px;}")


# class EmptyWidget(QWidget):
#     def __init__(self, parent=None):
#         super(EmptyWidget, self).__init__(parent)
#         lay = QVBoxLayout(self)
#         lay.addWidget()
#         pixmap = QPixmap(path).scaledToHeight(180)
#         label = QLabel(self.scrollAreaWidgetContents)
#         label.setPixmap(pixmap)
#         self.horizontalLayout.addWidget(label)