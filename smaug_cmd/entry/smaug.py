import logging
import sys
from typing import cast
from PySide6.QtCore import QObject, QSettings, QDir
from PySide6.QtWidgets import QApplication, QMessageBox

from smaug_cmd.ui import LogInDialog, AssetListDialog

from smaug_cmd import setting
from smaug_cmd.bootstrap import bootstrap
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.services import SmaugCmdLogic

logger = logging.getLogger('smaug_cmd')
logging.basicConfig(level=logging.DEBUG)


class SmaugUploaderApp(QObject):

    def __init__(self,):
        super(SmaugUploaderApp, self).__init__(None)
        self.logic = SmaugCmdLogic()
        self.settings = QSettings()
        
        self.login_ui = LogInDialog(settings=self.settings)

        self.asset_list = AssetListDialog(logic=self.logic, setting=self.settings)
        # self.asset_list.setToAssetTemplateCallback(self.logic.asset_template)
        self.asset_list.folder_tree_widget.setRootFolder(
            str(self.settings.value("rootFolder", QDir.homePath()))
        )
        
        self._connect()

    def _connect(self):
        self.login_ui.accountInfoRetrieved.connect(self._on_login)

    def _on_login(self, username, password):
        try:
            self.logic.log_in(username, password)
        except SmaugError as e:
            QMessageBox.critical(self.login_ui, "登入失敗", str(e))
            return

        self.login_ui.close()
        self._init()
        self.asset_list.show()

    def _init(self):
        pass

    def run(self):
        bootstrap(setting)
        self.login_ui.show()


if __name__ == "__main__":
    app = cast(QApplication, QApplication.instance())
    if not app:
        app = QApplication(sys.argv)
    if sys.platform == "win32":
        app.setStyle("Fusion") # ignore: E501
    app.setOrganizationName("MoonShine")
    app.setApplicationName("Smaug-Uploader")
    smaug_app = SmaugUploaderApp()
    smaug_app.run()
    app.exec()
