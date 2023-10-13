from PySide6.QtWidgets import QApplication

# import qtmodern.styles
# import qtmodern.windows

from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.ui import AssetEditorWidget


asset_linux: AssetTemplate = {
    "id": None,
    "name": "Tree_A",
    "categoryId": None,
    "previews": [
        "/home/deck/repos/smaug/storage/_source/Tree_A/Tree_A_Lowpoly.jpg"
    ],
    "renders": [
        "/home/deck/repos/smaug/storage/_source/Tree_A/Render/Tree_A_Lowpoly.jpg",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Render/Tree_A_Low.jpg"
    ],
    "models": [
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Tree_A_Low.ma",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Fbx/Tree_A_Low.fbx",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Obj/Tree_A_Low.obj",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Model/USD/Tree_A_Low.usd"
    ],
    "textures": [
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.tx",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.png",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.tx",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.png",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.tx",
        "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.jpg"
    ],
    "preview_model": "",
    "tags":[
        "fire", "tree", "plant"
    ]
}

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    my_widget = AssetEditorWidget()
    my_widget.setAsset(asset_linux)
    # qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(my_widget)
    # mw.show()
    my_widget.show()
    app.exec()