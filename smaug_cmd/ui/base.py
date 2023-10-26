# import sys

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import smaug_cmd_rc # noqa


class MoonFrame(QFrame):
    def __init__(self, parent=None):
        super(MoonFrame, self).__init__(parent)
        # if sys.platform == "win32":
        self.setStyleSheet("MoonFrame{border: 0px;}")


# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     window = EmptyWidget()
#     window.show()
#     sys.exit(app.exec())