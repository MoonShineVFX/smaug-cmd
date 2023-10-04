
import sys
from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication, QMessageBox

from smaug_cmd.ui import LogInDialog, UploadWidget, CategoryListWidget
# from smaug_cmd.domain.bootstrp import bootstrip
from smaug_cmd.domain.logic import UploadHandler


class SmaugUploaderApp(QObject):
    def __init__(self, settings:QSettings=None):
        super(SmaugUploaderApp, self).__init__(None)
        self.login_ui = LogInDialog()
        self.main_ui = UploadWidget()
        self.logic = UploadHandler(ui_widget=self.main_ui)
        self.catrgories_ui = CategoryListWidget(parent=self.main_ui)
        self.settings = settings
        self._connect()

    def _connect(self):
        self.login_ui.accountInfoRetrieved.connect(self._on_login)

    def _on_login(self, username, password):
        re = self.logic.log_in(username, password)
        if re[0] != 200:
            QMessageBox.critical(self.login_ui, "登入失敗", re[1]['message'])
            return

        self._init()
        self.main_ui.show()

    def _init(self):
        menus = self.logic.get_menus()
        for menu in menus:
            menu_tree = self.logic.get_menu_tree(menu['id'])
            self.catrgories_ui.addMenuTree(menu_tree)
    
    def run(self):
        self.login_ui.show()


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.setOrganizationName('MoonShine')
    app.setApplicationName('galaxy_uploader')
    upload_app = SmaugUploaderApp()
    upload_app.run()
    app.exec()
