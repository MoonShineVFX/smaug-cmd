from PySide6.QtCore import QThread, Signal, Slot
from smaug_cmd.model import data as ds


class MenuTreeThread(QThread):
    data_fetched = Signal(object)

    @Slot(str)
    def fetch_data(self, menu_id):
        data = ds.get_menuTree(menu_id)
        self.data_fetched.emit(data)


