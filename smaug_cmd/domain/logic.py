import logging
from typing import List, Optional, Tuple, Callable
from PySide6.QtCore import QObject

from smaug_cmd.domain.smaug_types import Menu, MenuTree
from smaug_cmd.model import login_in as api_login
from smaug_cmd.model import data as ds
from smaug_cmd.ui import UploadWidget

logger = logging.getLogger('smaug-cmd.domain')


class SmaugCmdHandler(QObject):
    
    def __init__(self, ui_widget: UploadWidget):
        pass

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb if er_cb(error_msg) else None

    def log_in(self, user_name, password) -> Tuple[int, dict]:
        return api_login(user_name, password)

    def get_menus(self, error_cb: Optional[Callable]) -> Optional[List[Menu]]:
        re = ds.get_menus()
        if str(re[0])[0] != '2':
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def get_menu_tree(self, menu_id, error_cb: Optional[Callable]=None)-> Optional[MenuTree]:
        re = ds.get_menu_tree(menu_id)
        if str(re[0])[0] != '2':
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]
    

    