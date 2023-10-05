
from PySide6.QtCore import  Signal
from PySide6.QtGui import  QColor, QPalette
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from smaug_cmd.ui import FlowLayout


class TagItem(QWidget):
    tagRemoved = Signal(str)

    def __init__(self, text):
        super(TagItem, self).__init__()

        # 建立佈局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        self.setLayout(layout)

        # 建立標籤
        self.label = QLabel(text, self)
        layout.addWidget(self.label)

        # 建立刪除按鈕
        self.remove_btn = QPushButton("X", self)
        self.remove_btn.setFixedSize(20, 20)  # 設定固定大小
        self.remove_btn.clicked.connect(self._onClicked)
        layout.addWidget(self.remove_btn)

        # 設定背景色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(100, 100, 250))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # 設定圓角邊框
        self.setStyleSheet("TagItem {border-radius: 4px;}")

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed) 

    def _onClicked(self):
        self.tagRemoved.emit(self.label.text())

    def text(self):
        return self.label.text()


class TagsWidget(QWidget):
    def __init__(self):
        super(TagsWidget, self).__init__()

        # 建立主要的垂直佈局
        main_layout = QVBoxLayout(self)

        # 建立 tag 的 FlowLayout
        self._layout = FlowLayout()

        # 使用 set 來存儲標籤
        self.tags_set = set()

        self.tag_input = QLineEdit(self)
        self.tag_input.setPlaceholderText("Enter a tag and press Enter...")
        self.tag_input.returnPressed.connect(self._onTagEntered)

        # 將輸入框加入到主要的垂直佈局中
        main_layout.addWidget(self.tag_input)

        # 增加 placeholder 和 tags 到 FlowLayout
        self.placeholder_label = QLabel("no tags yet", self)
        self._layout.addWidget(self.placeholder_label)
        
        main_layout.addLayout(self._layout)

    def _onTagEntered(self):
        tag_text = self.tag_input.text().strip()
        if tag_text and tag_text not in self.tags_set:
            self.addTag(tag_text)
        self.tag_input.clear()
        self._updatePlaceholder()

    def _updatePlaceholder(self):
        self.placeholder_label.setVisible(len(self.tags_set) == 0)

    def addTag(self, tag_text):
        tag_widget = TagItem(tag_text)
        tag_widget.tagRemoved.connect(self.removeTag)
        self._layout.addWidget(tag_widget)
        self.tags_set.add(tag_text)
        self._updatePlaceholder()

    def removeTag(self, tag_text):
        for index in range(self._layout.count()):
            widget = self._layout.itemAt(index).widget()
            if widget and isinstance(widget, TagItem) and widget.text() == tag_text:
                self.tags_set.remove(tag_text)  # 從 set 中移除標籤
                widget.deleteLater()  # 移除 widget
                break
        self._updatePlaceholder()


# 測試
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TagsWidget()
    window.show()
    sys.exit(app.exec())