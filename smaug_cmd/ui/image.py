from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QScrollArea, QLabel, QVBoxLayout


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._heigh = 220
        self._big_picture_frame=None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(0, 0, 380, self._heigh)
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
            label.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to hand when hovering over image
            label.mousePressEvent = lambda event, path=path: self.displayRawImage(path)
            self.horizontalLayout.addWidget(label)

    def displayRawImage(self, path):
        # If there's an existing dialog, close it before opening a new one
        if self._big_picture_frame:
            self._big_picture_frame.close()
        
        self._big_picture_frame = QDialog(self)
        self._big_picture_frame.setWindowTitle("Raw Image")
        self._big_picture_frame.setLayout(QVBoxLayout())
        label = QLabel(self._big_picture_frame)
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        self._big_picture_frame.layout().addWidget(label)
        
        # Capture the global position of the mouse click
        mouse_position = self.mapToGlobal(self.scrollAreaWidgetContents.mapFromGlobal(QCursor.pos()))

        # Get the dimensions of the dialog
        width = self._big_picture_frame.width()
        height = self._big_picture_frame.height()
        
        # Adjust the position of the dialog so it's centered on the click point
        self._big_picture_frame.move(mouse_position.x() - width // 2, mouse_position.y() - height // 2)
        self._big_picture_frame.exec_()
