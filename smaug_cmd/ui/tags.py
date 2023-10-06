from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
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

tag_item_qss = """
    QWidget {
        background-color: #6a0dad;
        border: 1px solid #9a32cd;
        border-top-left-radius: 4px;
        border-bottom-left-radius: 4px;
    }
    QLabel {
        color: #ffffff;
    }
    QPushButton {
        color: #6a0dad;
        background-color: #ffffff;
        border: 1px solid #6a0dad;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
    }
"""


class TagItem(QWidget):
    tagRemoved = Signal(str)

    def __init__(self, text):
        super(TagItem, self).__init__()

        # 建立佈局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 建立標籤
        font = QFont()
        font.setPointSize(10)
        self.label = QLabel(text, self)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # 建立刪除按鈕
        self.remove_btn = QPushButton("X", self)
        self.remove_btn.setFixedSize(20, 20)  # 設定固定大小
        layout.addWidget(self.remove_btn)

        # 設定背景色和邊框
        self.setAutoFillBackground(True)
        self.setStyleSheet(tag_item_qss)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.remove_btn.clicked.connect(self._onClicked)

    def _onClicked(self):
        self.tagRemoved.emit(self.label.text())

    def text(self):
        return self.label.text()


class TagsWidget(QWidget):
    def __init__(self):
        super(TagsWidget, self).__init__()

        # 建立主要的垂直佈局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # 建立 tag 的 FlowLayout
        self.f_lay = FlowLayout()

        # 使用 set 來存儲標籤
        self.tags_set = set()

        self.tag_input = QLineEdit(self)
        self.tag_input.setPlaceholderText("Enter a tag and press Enter...")
        self.tag_input.returnPressed.connect(self._onTagEntered)

        # 將輸入框加入到主要的垂直佈局中
        main_layout.addWidget(self.tag_input)

        # 增加 placeholder 和 tags 到 FlowLayout
        self.placeholder_label = QLabel(" no tags yet")
        self.f_lay.addWidget(self.placeholder_label)

        main_layout.addLayout(self.f_lay)

    def _onTagEntered(self):
        tag_text = self.tag_input.text().strip()
        if tag_text and tag_text not in self.tags_set:
            self.addTag(tag_text)
        self.tag_input.clear()
        self._updatePlaceholder()

    def _updatePlaceholder(self):
        # 獲取佈局中的第一個部件
        first_widget = self.f_lay.itemAt(0).widget() if self.f_lay.count() > 0 else None

        if len(self.tags_set) == 0 and first_widget != self.placeholder_label:
            self.f_lay.addWidget(self.placeholder_label)
            self.placeholder_label.show()
        elif first_widget == self.placeholder_label:
            self.f_lay.removeWidget(self.placeholder_label)
            self.placeholder_label.hide()

    def addTag(self, tag_text):
        tag_widget = TagItem(tag_text)
        tag_widget.tagRemoved.connect(self.removeTag)
        self.f_lay.addWidget(tag_widget)
        self.tags_set.add(tag_text)
        self._updatePlaceholder()

    def removeTag(self, tag_text):
        for index in range(self.f_lay.count()):
            widget = self.f_lay.itemAt(index).widget()
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
