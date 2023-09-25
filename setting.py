import os

api_root = os.environ["API_URL"]  # 資料庫位置


model_extensions = [
    "ma",
    "mb",
    "blend",
    "max",
    "c4d",
    "obj",
    "mtl",
    "fbx",
    "dae",
    "3ds",
    "usd",
    "usda",
    "usdz",
]

texture_extensions = ["tx", "png", "jpg", "jpeg", "tga", "bmp"]
# 合法的貼圖副檔名

texture_factors = ["textures", "texture", "maps", "map"]
# 完整檔名中有 texture_factor 裡的元素會被視為預覽圖

render_factors = ["render", "renders", "image", "images"]


preview_factors = [
    "preview",
]
# 完整檔名中有preview的檔案會被視為預覽圖
