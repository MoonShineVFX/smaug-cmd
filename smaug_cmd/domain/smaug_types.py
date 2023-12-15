from enum import Enum
from datetime import date
from typing import Dict, Literal, TypedDict, List, Optional
from PySide6.QtCore import Qt


CategoryRole = Qt.ItemDataRole.UserRole + 1


TEXTURE_GROUP_KEYWORDS = Literal["2K", "4K"]


SOFTWARE_CATEGORIRS = {
    "3dsmax": ["max"],
    "blender": ["blend"],
    "c4d": ["c4d"],
    "fbx": ["fbx"],
    "maya": ["mb", "ma"],
    "obj": ["obj", "mtl"],
    "unreal": ["uasset"],
    "usd": ["usd"],
}

REVERSE_SOFTWARE_CATEGORIRS = {
    "blend": "blender",
    "c4d": "c4d",
    "fbx": "fbx",
    "ma": "maya",
    "max": "3dsmax",
    "mb": "maya",
    "mtl": "obj",
    "obj": "obj",
    "uasset": "unreal",
    "usd": "usd",
}


RepresentationType = Literal["MODEL", "PREVIEW", "RENDER", "TEXTURE"]
RepresentationFormat = Literal[
    "IMG", "FBX", "GLB", "MAX", "MB", "OBJ", "C4D", "UNREAL", "BLEND", "USD", "MIX"
]

class AssetTemplate(TypedDict):
    id: Optional[int]
    name: str
    categoryId: Optional[int]
    previews: List[str]  # 預覽圖
    preview_model: str  # 預覽模型
    models: List[str]  # 模型
    textures: List[str]  # 貼圖
    renders: List[str]  # 渲染圖
    meta: Dict[str, str]  # 其他資料(如果有)
    tags: List[str]  # 標籤
    basedir: str  # 資料夾路徑
    createAt: Optional[str]
    updateAt: Optional[str]


class AssetDBTemplate(TypedDict):
    id: Optional[int]
    name: str
    categoryId: Optional[int]
    previews: List[str]  # 預覽圖
    preview_model: str  # 預覽模型
    models: List[Dict[str, str]]  # 模型
    textures: List[Dict[str, str]]  # 貼圖
    renders: List[str]  # 渲染圖

    tags: List[str]  # 標籤
    # basedir: str  # 資料夾路徑
    createAt: date
    updateAt: Optional[date]


class AssetCreateResponse(TypedDict):
    id: str
    name: str
    creatorId: str
    categoryId: int
    createAt: date
    updateAt: Optional[date]


class AssetFolderType(Enum):
    """Enum for the type of asset folder."""

    UNKNOWN = 0
    RESOURCE_DEPART = 1
    ASSET_DEPART = 2


class ResourceFolderType(Enum):
    """Enum for the type of resource folder."""

    UNKNOWN = 0
    
    AVALON_SOURCE_MODEL = 1
    # 目錄下有多張 preview 圖片
    # 目錄下會有 _AvalonSource 資料夾,
    # 目錄下有 _AvalonSource 目錄
    # _AvalonSource 下會有數個 texture 目錄，通常名為texture, texture_low, ...等等， 並包含多個 dcc 檔案
    # 至少要有一個 dcc 檔跟一個貼圖檔
    # _AvalonSource 下會有 preview 檔，需排除
    # dcc 檔可能有變體, 例加有後綴 _low 的模型檔案, Optional
    # 範例目錄：
    #     _Asset\MoonshineProject_2019_Obsidian\201903_Jdb\Prop\Bag
    #     _Asset\MoonshineProject_2020_Obsidian\202007_LianYue\Props\Backpack

    NORMAL_RESOURCE_MODEL = 2
    # 資料夾下有一個貼圖目錄，名字可能為 Texture、tex, 
    # 資料夾下有多個 dcc 檔案
    # 資料夾下有複數 preview 圖片
    # 有時也會在 folder_path 下有一個 Texture_JPG 資料夾，放置轉為 JPG 的貼圖檔案，這個資料夾為 Optinoal
    # 在指定該有 dcc 檔的地方應該最少要有一個 dcc 檔案
    # 在指定該有貼圖的地方最少要有一個貼圖檔案
    # 範例目錄：
    #     _Asset\MoonshineProject_2019\BundleProject_TheBeltAndRoad\TheBeltAndRoad\Environment\ChangAnGate
    #     _Asset\MoonshineProject_2020_Obsidian\202003_AdventureLemon\jianguo

    DOWNLOAD_VARIANT1_MODEL = 3
    # 資料夾下數個以 `uploads_files_` 開頭的資料夾，內含貼圖跟 dcc 檔，該資料夾的名稱 `+` 替代 ` `(空白)
    # 資料夾下也有 preview 圖片

    # example: 
    #     _Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\parachute
    #     _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
    #     _Asset\MoonshineProject_2020_Obsidian\202001_AsusBrandVideo4\Buy\Sci+Fi+Power+Suit

    DOWNLOAD_VARIANT2_MODEL = 4
    # 資料夾下有一個 `"asset 名稱"_textures` 的資料夾，內含貼圖，
    # 資料夾下有多個 dcc 檔案
    # 資料夾下有複數 preview 圖片

    # example: 
    #     _Asset\MoonshineProject_2020_Obsidian\202006_FetNetwork\parachute
    
    THREE_MAX_MODEL = 5
    
    TAIWAN_CULTURE = 6
    # 資料夾下有 dcc 檔，通常為 fbx
    # 資料夾下有數個 preview 圖檔
    # 有 3D 目錄, 下有其他的 dcc 檔
    # 有 texture 目錄, 下有貼圖
    # 有 Preview 目錄, 目錄裡的也是 preview 圖檔
    # 有 Render 目錄, 下有 render 出來的圖檔

    # example: 
    #     _Asset\Source_Taiwan\Culture01\BTStation_HighPoly

    UASSET_MODEL = 7

class CategoryTree(TypedDict):
    id: str
    name: str
    children: List["CategoryTree"]


class CategoryDetailTree(TypedDict):
    id: int
    name: str
    parentId: int
    createAt: date
    updateAt: date
    isVisible: bool
    menuId: str
    path: str
    breadCrumb: str


class Menu(TypedDict):
    id: str
    name: str


class MenuTree(TypedDict):
    id: str
    name: str
    iconName: str
    children: List["CategoryTree"]


class Representation(TypedDict):
    assetId: str
    name: str
    type: RepresentationType
    format: RepresentationFormat
    path: str
    fileSize: int
    uploaderId: str


class Asset(TypedDict):
    name: str
    categoryId: int
    representations: List[Representation]
    tags: List[str]


class AssetCreateParams(TypedDict):
    name: str
    categoryId: int
    tags: List[str]


class RepresentationCreateParams(TypedDict):
    assetId: str
    name: str
    type: RepresentationType
    format: RepresentationFormat
    path: str
    fileSize: int
    uploaderId: str
    meta: Dict[str, str]


class RepresentationCreateResponse(TypedDict):
    id: int
    createAt: date
    uploadAt: Optional[date]
    assetId: str
    name: str
    type: RepresentationType
    format: RepresentationFormat
    path: str
    fileSize: int
    uploaderId: str
    textureId: Optional[str]


class UserInfo(TypedDict):
    id: str
    name: str
    email: str
    picture: str
    account: str
    roleId: str
    roleName: str
    type: str
    updateAt: Optional[date]
    createAt: date
    extenData: Dict[str, str | int]
