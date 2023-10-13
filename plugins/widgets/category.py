from PySide6.QtCore import Qt
from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

from smaug_cmd.ui import CategoryListWidget

class MyCustomButtonPlugin(QDesignerCustomWidgetInterface):

    def __init__(self, parent=None):
        super(MyCustomButtonPlugin, self).__init__(parent)
        self._initialized = False

    def initialize(self, core):
        if self._initialized:
            return
        self._initialized = True

    def isInitialized(self):
        return self._initialized

    def name(self):
        return "CategoryListWidget"

    def group(self):
        return "MoonShine Widgets"

    def icon(self):
        return QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def includeFile(self):
        return "your_custom_widget_file"

    def createWidget(self, parent):
        return CategoryListWidget(parent)