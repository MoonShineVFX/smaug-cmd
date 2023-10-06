from PySide6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(0, 0, 380, 180)
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

    def setPictures(self, image_paths):
        # 清空既有的widgets，以確保新圖片將會被加入
        for i in reversed(range(self.horizontalLayout.count())):
            widget = self.horizontalLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for path in image_paths:
            pixmap = QPixmap(path).scaledToHeight(180)
            label = QLabel(self.scrollAreaWidgetContents)
            label.setPixmap(pixmap)
            self.horizontalLayout.addWidget(label)
