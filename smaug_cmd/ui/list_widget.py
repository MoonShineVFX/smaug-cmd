from typing import List, Optional
import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QApplication
import smaug_cmd_rc  # noqa: F401


class FileListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.file_list_widget = QListWidget()

        # 設置為圖標模式
        self.file_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.file_list_widget.setContentsMargins(2,2,2,2)
        self._layout.addWidget(self.file_list_widget)
        self.setLayout(self._layout)

    def setFiles(self, files: Optional[List[str]]):
        # 先清空現有的列表項目
        self.file_list_widget.clear()
        
        # 添加新的文件列表項目
        for file in files:
            # 獲取文件的副檔名S
            file_name = os.path.basename(file)
            file_extension = os.path.splitext(file)[-1].lower()
            
            item = QListWidgetItem(file_name)
            item.setToolTip(file)

            icon_path = f":/icon/icon{file_extension}.png"
            if not os.path.exists(icon_path):
                icon_path = ":/icon/icon.default.png"

            item.setIcon(QIcon(icon_path))
            self.file_list_widget.addItem(item)

    def clear(self):
        self.file_list_widget.clear()


if __name__ == '__main__':
    app = QApplication([])
    window = FileListWidget()
    
    model_files = [
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Tree_A_Low.ma",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Fbx/Tree_A_Low.fbx",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Obj/Tree_A_Low.obj",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/USD/Tree_A_Low.usd"
    ]

    window.setFiles(model_files)
    window.show()
    sys.exit(app.exec())


