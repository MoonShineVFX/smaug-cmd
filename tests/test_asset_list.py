from PySide6.QtWidgets import QApplication
from smaug_cmd.ui import AssetListDialog


if __name__ == '__main__':
    import sys

    app = QApplication.instance()
    if not app:
        app = QApplication()
    if sys.platform == "win32":
        app.setStyle("Fusion")
        # app.setStyleSheet("""
        #     QFrame{border: 1px solid gray;}}
        #     """)
    my_widget =AssetListDialog()
    my_widget.show()
    app.exec()