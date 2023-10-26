from PySide6.QtWidgets import QWidget
from smaug_cmd.designer.empty_widget_ui import Ui_empty_frame


class EmptyWidget(QWidget, Ui_empty_frame):
    def __init__(self, parent=None):
        super(EmptyWidget, self).__init__(parent)
        self.setupUi(self)