
import sys
from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication

from smaug_cmd.ui import LogInDialog, UploadWidget, CategoryListWidget
from smaug_cmd.domain.bootstrp import bootstrip
from smaug_cmd.domain.logic import UploadHandler


class SmaugUploader(QObject):
    def __init__(self, settings:QSettings=None):
        super(SmaugUploader, self).__init__(None)
        self.logic = UploadHandler()
        self.login_ui = LogInDialog()
        self.main_ui = UploadWidget()
        self.catrgories_ui = CategoryListWidget(parent=self.main_ui)
        self.settings = settings
        self._connect()

    def _connect(self):
        self

    def _init_categories(self):
        self.catrgories_ui.set_categories(self.logic.get_menus())
    
    def run(self):
        self._login
        self.ui = UploadWidget()
        self._upload_widget.show()


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.setOrganizationName('MoonShine')
    app.setApplicationName('galaxy_uploader')
    upload_app = SmaugUploader()
    upload_app.run()
    app.exec_()
