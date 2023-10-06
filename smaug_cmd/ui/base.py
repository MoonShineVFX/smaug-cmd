import sys

from PySide6.QtWidgets import QFrame


class MoonFrame(QFrame):
    def __init__(self, parent=None):
        super(MoonFrame, self).__init__(parent)
        if sys.platform == "win32":
            self.setStyleSheet("MoonFrame{border: 0px;}") 