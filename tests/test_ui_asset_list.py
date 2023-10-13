from PySide6.QtWidgets import QApplication
from smaug_cmd.ui import AssetListDialog


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    my_widget =AssetListDialog()
    my_widget.show()
    app.exec()