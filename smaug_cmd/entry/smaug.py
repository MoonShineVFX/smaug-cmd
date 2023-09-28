
import sys
from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication
from smaug_cmd.ui.uploader_widget import UploadWidget
from smaug_cmd.domain.logic import UploadHandler


class SmaugUploader(QObject):
    def __init__(self, settings:QSettings=None):
        super(SmaugUploader, self).__init__(None)
        self._upload_widget = None
        self._settings = settings

    def run(self):
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
