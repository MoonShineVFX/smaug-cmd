from typing import Tuple
from PySide6.QtCore import QObject

from smaug_cmd.domain.smaug_types import MenuTree
from smaug_cmd.model import login_in as api_login
from smaug_cmd.model import data as ds


class UploadHandler(QObject):
    def __init__(self, ui_widget):
        self._ui = ui_widget
        self.__is_uploading = False

    def log_in(self, user_name, password) -> Tuple[int, dict]:
        return api_login(user_name, password)

    def get_menus(self):
        menus = ds.get_menus()
        return menus

    def get_menu_tree(self, menu_id)-> MenuTree:
        tree = ds.get_menu_tree(menu_id)
        return tree

