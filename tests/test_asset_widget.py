
import sys
from PySide6.QtWidgets import QApplication
from smaug_cmd.ui.asset_widget import AssetWidget

app = QApplication(sys.argv)
asset_widget = AssetWidget()
asset_widget.show()
sys.exit(app.exec_())