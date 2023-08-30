from smaug_cmd.entry.to_json import is_texture, is_preview, is_model, is_render_image, directory_to_json

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


def test_is_preview():
    for path in mock_assets_path_linux:
        assert is_preview(path) == mock_assets_path_linux[path]["is_preview"]
    # assert not is_preview(r"c:\preview")
    # assert not is_preview(r"c:\preview.png")
    # assert is_preview(r"c:\a123\preview.jpg")
    # assert is_preview(r"c:\a123\a123_preview.jpeg")
    # assert is_preview(r"c:\a123\a123.tga")
    # assert is_preview(r"c:\b456\a123\a123preview.bmp")


def test_is_texture():
    for path in mock_assets_path_linux:
        assert is_texture(path) == mock_assets_path_linux[path]["is_texture"]
    # assert not is_texture(r"c:\texture")
    # assert not is_texture(r"c:\texture.png")
    # assert not is_texture(r"c:\a123\texture.jpg")
    # assert not is_texture(r"c:\b456\a123\a123texture.bmp")
    # assert is_texture(r"c:\a123\texture\a1_normal.png")
    # assert is_texture(r"c:\a123\maps\a123_diffuse.tga")
    # assert is_texture(r"c:\a123\maps\brick.tga")


def test_is_model():
    for path in mock_assets_path_linux:
        assert is_model(path) == mock_assets_path_linux[path]["is_model"]
    # assert not is_model(r"c:\model")
    # assert not is_model(r"c:\model.png")
    # assert not is_model(r"c:\a123\model.jpg")
    # assert is_model(r"c:\a123\maps\a1.ma")
    # assert is_model(r"c:\a123\maps\a1.ma")
    # assert is_model(r"c:\b456\a123\a123model.mb")


def test_is_render_image():
    for path in mock_assets_path_linux:
        assert is_render_image(path) == mock_assets_path_linux[path]["is_render"]