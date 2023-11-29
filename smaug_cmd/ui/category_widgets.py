from typing import List, Optional
import logging
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QBrush
from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from smaug_cmd.domain.smaug_types import MenuTree, CategoryTree, CategoryRole

logger = logging.getLogger('smaug-cmd.ui')


class CategoryListWidget(QWidget):
    selectedCategoryId = Signal(int)

    def __init__(self, parent=None, categroies=None):
        super(CategoryListWidget, self).__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.tw = QTreeWidget()
        self.tw.setColumnCount(2)
        self.tw.setHeaderLabels(['Name', 'Id'])
        self._menu_trees: List[MenuTree] = []
        mlay = QVBoxLayout()
        self.setLayout(mlay)
        mlay.addWidget(self.tw)
        self.setWindowTitle('Category Selector')
        self._categroies = categroies
        self._update()
        self.tw.itemClicked.connect(self._on_item_clicked)

    def _update(self):
        self.tw.clear()
        if len(self._menu_trees) > 1:
            self._menu_trees = sorted(self._menu_trees, key=lambda x: x['name'])
        
        for menu_tree in self._menu_trees:
            item_list: List[QTreeWidgetItem] = list()
            menu_item = QTreeWidgetItem([menu_tree['name']])
            if menu_tree['children'] is not []:
                categort_tree = menu_tree['children']
                self._add_cate_r(categort_tree, menu_item, item_list)
            # self.tw.addTopLevelItems(item_list)
            self.tw.addTopLevelItem(menu_item)
        
        logger.debug(self.tw.topLevelItemCount())
        if self.tw.topLevelItemCount() > 0:
            for i in range(self.tw.topLevelItemCount()):
                self.tw.expandItem(self.tw.topLevelItem(i))
            self.tw.resizeColumnToContents(0)
            self.tw.resizeColumnToContents(1)

    def _expand_all_items(self, item:QTreeWidgetItem):
        self.tw.expandItem(item)
        for i in range(item.childCount()):
            child_item = item.child(i)
            self._expand_all_items(child_item)

    def _add_cate_r(self, categoryTrees:List[CategoryTree], parent_node:QTreeWidgetItem, item_list:List[QTreeWidgetItem]):
        item_list.append(parent_node)
        for cate in categoryTrees:
            cate_item = QTreeWidgetItem([cate['name'], str(cate['id'])])
            cate_item.setData(0, CategoryRole, cate)
            item_list.append(cate_item)
            parent_node.addChild(cate_item)
            if cate['children'] is not []:
                self._add_cate_r(cate['children'], cate_item, item_list)

    def addMenuTree(self, menu_tree:Optional[MenuTree]=None):
        print('addMenuTree')
        if not menu_tree:
            return
        self._menu_trees.append(menu_tree)
        self._update()

    def _on_item_clicked(self, item, column):
        logger.debug(f'click on: {item.text(column)}')
        cate = item.data(0, CategoryRole)
        if cate:
            self._animate_select(item)
            logger.debug(f'emit selecteCategoryId: {cate["id"]}')
            self.selectedCategoryId.emit(cate['id'])

    def _animate_select(self, item:QTreeWidgetItem):
        original_color = item.background(0)
        item.setBackground(0, QBrush(Qt.GlobalColor.green))
        def restore_color():
            item.setBackground(0, QBrush(original_color))
        QTimer.singleShot(200, restore_color)
        