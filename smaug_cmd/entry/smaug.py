import logging
import sys

from PySide6.QtCore import QObject, QSettings, QDir
from PySide6.QtWidgets import QApplication, QMessageBox

from smaug_cmd.ui import LogInDialog, AssetListDialog

from smaug_cmd import setting
from smaug_cmd.bootstrap import bootstrap
from smaug_cmd.domain.logic import SmaugCmdHandler

logger = logging.getLogger('smaug-cmd')
logging.basicConfig(level=logging.DEBUG)


class SmaugUploaderApp(QObject):

    def __init__(self,):
        super(SmaugUploaderApp, self).__init__(None)
        self.current_user = None
        self.logic = SmaugCmdHandler()
        self.settings = QSettings()

        self.login_ui = LogInDialog()

        self.asset_list = AssetListDialog(logic=self.logic)
        self.asset_list.setToAssetTemplateCallback(self.logic.asset_template)
        self.asset_list.folder_tree_widget.setRootFolder(
            str(self.settings.value("rootFolder", QDir.homePath()))
        )
        
        self._connect()

    def _connect(self):
        self.login_ui.accountInfoRetrieved.connect(self._on_login)

    def _on_login(self, username, password):
        re = self.logic.log_in(username, password)
        if re is None or re[0] != 200:
            QMessageBox.critical(self.login_ui, "登入失敗", re[1]["message"])
            return
        self.current_user = re[1]
        self.login_ui.close()
        self._init()
        self.asset_list.show()

    def _init(self):
        pass

    def run(self):
        bootstrap(setting)
        self.login_ui.show()


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    if sys.platform == "win32":
        app.setStyle("Fusion")
    app.setOrganizationName("MoonShine")
    app.setApplicationName("Smaug-Uploader")
    smaug_app = SmaugUploaderApp()
    smaug_app.run()
    app.exec()
