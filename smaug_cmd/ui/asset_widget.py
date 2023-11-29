import logging
from PySide6.QtWidgets import QStackedWidget
from smaug_cmd.designer.asset_widget_ui import Ui_asset_widget

logget = logging.getLogger("smaug-cmd.ui.asset_widget")


class AssetWidget(QStackedWidget, Ui_asset_widget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        self.setupUi(self)
        # self.setTabOrder(False)
        return

    def setAsset(self, asset_template):
        logget.debug("set asset: %s", asset_template)

        if asset_template is None:
            self.setCurrentWidget(self.empty_page)
            return
        self.asset_page.setAsset(asset_template)
        self.setCurrentWidget(self.asset_page)
        return
