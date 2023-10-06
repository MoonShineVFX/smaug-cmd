import logging
import sys

from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication, QMessageBox

from smaug_cmd.ui import LogInDialog, CategoryListWidget, AssetListDialog

# from smaug_cmd.domain.bootstrp import bootstrip
from smaug_cmd.domain.logic import SmaugCmdHandler

logger = logging.getLogger('smaug-cmd')
logging.basicConfig(level=logging.DEBUG)


class SmaugUploaderApp(QObject):
    def __init__(self, settings: QSettings = None):
        super(SmaugUploaderApp, self).__init__(None)
        self.current_user = None
        self.login_ui = LogInDialog()
        self.assets_view_ui = AssetListDialog()
        self.logic = SmaugCmdHandler()
        self.settings = settings
        self._connect()

    def _connect(self):
        self.login_ui.accountInfoRetrieved.connect(self._on_login)

    def _on_login(self, username, password):
        re = self.logic.log_in(username, password)
        if re[0] != 200:
            QMessageBox.critical(self.login_ui, "登入失敗", re[1]["message"])
            return
        self.current_user = re[1]
        self.login_ui.close()
        self._init()
        self.assets_view_ui.show()

    def _init(self):
        pass
        # menus = self.logic.get_menus()
        # for menu in menus:
        #     logger.debug(f"menu: {menu}")
        #     menu_tree = self.logic.get_menu_tree(menu["id"])
        #     if menu_tree is None:
        #         continue
        #     self.catrgories_ui.addMenuTree(menu_tree)

    def run(self):
        self.login_ui.show()


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.setOrganizationName("MoonShine")
    app.setApplicationName("galaxy_uploader")
    smaug_app = SmaugUploaderApp()
    smaug_app.run()
    app.exec()
