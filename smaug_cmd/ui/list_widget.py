from typing import List, Optional
import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QApplication


class FileListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.file_list_widget = QListWidget()

        # 設置為圖標模式
        self.file_list_widget.setViewMode(QListWidget.ViewMode.IconMode)

        self.layout.addWidget(self.file_list_widget)
        self.setLayout(self.layout)

    def setFiles(self, files: Optional[List[str]]):
        # 先清空現有的列表項目
        self.file_list_widget.clear()
        
        # 添加新的文件列表項目
        for file in files:
            item = QListWidgetItem(file)
            # 獲取文件的副檔名
            file_extension = os.path.splitext(file)[-1].lower()

            icon_path = f"path/to/icon{file_extension}.png"
            if not os.path.exists(icon_path):
                icon_path = "path/to/icon.default.png"

            item.setIcon(QIcon(icon_path))
            self.file_list_widget.addItem(item)

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


