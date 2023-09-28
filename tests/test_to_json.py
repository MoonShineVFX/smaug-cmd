import os

from smaug_cmd.domain.parsing import directory_to_json, is_model, is_preview, is_render_image, is_texture

mock_assets_path_linux = {
    "/home/deck/repos/smaug/storage/_source/Tree_A/Tree_A_Lowpoly.jpg": {
        "is_texture": False,
        "is_preview": True,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/MAYA2020.4.txt": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Tree_A_Low.ma": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Tree_A.ma": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Tree_A_Lowpoly.jpg": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/.mayaSwatches/Tree_A.ma.swatches": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Fbx/Tree_A_Low.fbx": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/USD/Tree_A_Low.usd": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Obj/Tree_A_Low.mtl": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Model/Obj/Tree_A_Low.obj": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.png": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.png": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.jpg": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Trunk_Low_Basecolor.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Color2.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Color.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/archmodels58_031_Pinus_strobus_bark_color.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Mask.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Basecolor.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Trunk_Low_color.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/.mayaSwatches/Mask2.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Render/Tree_A_Low.jpg": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": True,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Render/Tree_A_Lowpoly.jpg": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": True,
    },
    "/home/deck/repos/smaug/storage/_source/Tree_A/Render/Thumbs.db": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
}

mock_assets_path_win = {
    "D:/repos/smaug-cmd/_source/Tree_A/Model/USD/Tree_A_Low.usd": {
        "is_texture": False,
        "is_preview": False,
        "is_model": True,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Render/Thumbs.db": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Render/Tree_A_Low.jpg": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": True,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.png": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.png": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Mask.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.jpg": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/Tree_A_Trunk_Low_Basecolor.tx": {
        "is_texture": True,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/archmodels58_031_Pinus_strobus_bark_color.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Color2.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Mask2.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Basecolor.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Color.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Leaf_Low_Mask.png_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Trunk_Low_Basecolor.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
    "D:/repos/smaug-cmd/_source/Tree_A/Texture/2K/.mayaSwatches/Tree_A_Trunk_Low_color.jpg_hcm.swatch": {
        "is_texture": False,
        "is_preview": False,
        "is_model": False,
        "is_render": False,
    },
}

mock_assets_path = mock_assets_path_win if os.name == "nt" else mock_assets_path_linux


def test_is_preview():
    for path in mock_assets_path:
        assert is_preview(path) == mock_assets_path[path]["is_preview"]


def test_is_texture():
    for path in mock_assets_path:
        assert is_texture(path) == mock_assets_path[path]["is_texture"]


def test_is_model():
    for path in mock_assets_path:
        assert is_model(path) == mock_assets_path[path]["is_model"]


def test_is_render_image():
    for path in mock_assets_path:
        assert is_render_image(path) == mock_assets_path[path]["is_render"]


def test_directory_to_json():
    excepted_json_win = {
        "previews": ["D:/repos/smaug-cmd/_source/Tree_A/Tree_A_Lowpoly.jpg"],
        "preview_model": None,
        "models": [
            "D:/repos/smaug-cmd/_source/Tree_A/Model\\Tree_A_Low.ma",
            "D:/repos/smaug-cmd/_source/Tree_A/Model\\Fbx\\Tree_A_Low.fbx",
            "D:/repos/smaug-cmd/_source/Tree_A/Model\\Obj\\Tree_A_Low.mtl",
            "D:/repos/smaug-cmd/_source/Tree_A/Model\\Obj\\Tree_A_Low.obj",
            "D:/repos/smaug-cmd/_source/Tree_A/Model\\USD\\Tree_A_Low.usd",
        ],
        "textures": [
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Leaf_Low_Basecolor.png",
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Leaf_Low_Basecolor.tx",
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Leaf_Low_Mask.png",
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Leaf_Low_Mask.tx",
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Trunk_Low_Basecolor.jpg",
            "D:/repos/smaug-cmd/_source/Tree_A/Texture\\2K\\Tree_A_Trunk_Low_Basecolor.tx",
        ],
        "meta": {},
    }
    excepted_json = excepted_json_win
    asset_json = directory_to_json("D:/repos/smaug-cmd/_source/Tree_A/")
    assert asset_json == excepted_json


