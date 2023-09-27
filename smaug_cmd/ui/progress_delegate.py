from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import (
    QApplication,
    QStyle,
    QStyleOptionProgressBar,
    QStyledItemDelegate,
)


class ProgressDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ProgressDelegate, self).__init__(parent)
        self._maxHeight = 48

    def paint(self, painter, option, index):
        if index.column() == 1:
            progress = index.data()

            progressBarOption = QStyleOptionProgressBar()
            temp_rect = option.rect
            if temp_rect.width() > self._maxHeight:
                progress_rect = self._trans_rect(temp_rect)
            else:
                progress_rect = option.rect

            progressBarOption.rect = progress_rect  # 設定要畫的範圍
            progressBarOption.minimum = 0
            progressBarOption.maximum = 100
            progressBarOption.progress = progress
            progressBarOption.text = str(progress) + "%"
            progressBarOption.textVisible = True
            progressBarOption.textAlignment = Qt.AlignCenter

            QApplication.style().drawControl(
                QStyle.CE_ProgressBar, progressBarOption, painter
            )
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def _trans_rect(self, rect):
        if rect.height() > self._maxHeight:
            new_height = 48
            new_y = (rect.height() - 48) / 2 + rect.y()
            return QRect(rect.x(), new_y, rect.width(), new_height)
        else:
            return rect
