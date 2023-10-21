import sys
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QFileDialog, QPushButton, QVBoxLayout, QWidget


class FolderSelector(QWidget):
    folderSelected = Signal(str)  # 自定義訊號

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Folder Selector')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.select_button = QPushButton('Select Folder')
        self.select_button.setMinimumSize(0, 32)
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select a folder', '/path/to/start/from')
        if folder:  # 如果用戶選擇了一個資料夾而非取消
            self.folderSelected.emit(folder)  # 發射訊號

    def setText(self, text):
        self.select_button.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FolderSelector()

    # 連接自定義的 folderSelected 訊號到一個槽函數
    window.folderSelected.connect(lambda folder_path: print(f'Selected folder is: {folder_path}'))

    window.show()

    sys.exit(app.exec())