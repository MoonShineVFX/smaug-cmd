from enum import Enum
from datetime import date, datetime
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
    "IMG", "FBX", "GLB", "MAX", "MB", "OBJ", "C4D", "UNREAL", "BLEND", "USD"
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
    AVALON_SOURCE = 1
    NORMAL_SOURCE_FOLDER = 2
    DOWNLOAD_VARIANT1 = 3
    DOWNLOAD_VARIANT2 = 4
    MAXFOLDER = 5


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
