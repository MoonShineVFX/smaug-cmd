from typing import List
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from smaug_cmd.domain.smaug_types import MenuTree, CategoryTree


class CategoryListWidget(QWidget):
    selecteCategory = Signal(object)

    def __init__(self, parent=None, categroies=None):
        super(CategoryListWidget, self).__init__(parent)
        self.tw = QTreeWidget()
        self.tw.setColumnCount(2)
        self.tw.setHeaderLabels(['Name', 'Id'])
        self._menu_trees: List[MenuTree] = []
        mlay = QVBoxLayout()
        self.setLayout(mlay)
        mlay.addWidget(self.tw)
        self._categroies = categroies
        self._update()

    def _update(self):
        self.tw.clear()
        if len(self._menu_trees) > 1:
            self._menu_trees = sorted(self._menu_trees, key=lambda x: x['name'])
        
        for menu_tree in self._menu_trees:
            item_list = list()
            menu_item = QTreeWidgetItem([menu_tree['name']])
            if menu_tree['children'] is not []:
                categort_tree = menu_tree['children']
                self._add_cate_r(categort_tree, menu_item, item_list)
            self.tw.addTopLevelItems(item_list)

    def _add_cate_r(self, categoryTrees:List[CategoryTree], parent_node:QTreeWidgetItem, item_list:List[QTreeWidgetItem]):
        item_list.append(parent_node)
        for cate in categoryTrees:
            cate_item = QTreeWidgetItem([cate['name'], cate['id']])
            item_list.append(cate_item)
            parent_node.addChild(cate_item)
            if cate['children'] is not []:
                self._add_cate_r(cate['children'], cate_item, item_list)

    def addMenuTree(self, menu_tree:MenuTree=None):
        print('addMenuTree')
        if not menu_tree:
            return
        self._menu_trees.append(menu_tree)
        self._update()
        
        

