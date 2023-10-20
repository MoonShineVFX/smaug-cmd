from enum import Enum
from datetime import date
from typing import Optional
from PySide6.QtCore import Qt
from typing import Dict, Literal, TypedDict, List


CategoryRole = Qt.ItemDataRole.UserRole + 1


TEXTURE_GROUP_KEYWORDS = Literal["2K", "4K"]


SOFTWARE_CATEGORIRS = {
    "maya": [".mb", ".ma"],
    "3dsmax": [".max"],
    "unreal": [".uasset"],
    "fbx": [".fbx"],
    "c4d": [".c4d"],
    "obj": [".obj", ".mtl"],
    "usd": [".usd"],
}

REPRESENTATION_TYPE = Literal["MODEL", "PREVIEW", "RENDER", "TEXTURE"]


REPRESENTATION_FORMAT = Literal["IMG", "FBX", "GLB", "MAX", "MB", "OBJ", "C4D", "UNREAL", "USD"]


class AssetTemplate(TypedDict):
    id: Optional[int]
    name: str
    categoryId: Optional[int]
    previews: List[str]     # 預覽圖
    preview_model: str      # 預覽模型
    models: List[str]       # 模型
    textures: List[str]     # 貼圖
    renders: List[str]      # 渲染圖
    meta: Dict[str, str]    # 其他資料(如果有)
    tags: List[str]         # 標籤


class AssetFolderType(Enum):
    """Enum for the type of asset folder."""
    UNKNOWN = 0
    RESOURCE_DEPART = 1
    ASSET_DEPART = 2


class CategoryTree(TypedDict):
    id: str
    name: str
    children: List['CategoryTree']


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
    children: List['CategoryTree']


RepresentationType = Literal["MODEL", "PREVIEW", "RENDER", "TEXTURE"]
RepresentationFormat = Literal["IMG", "FBX", "GLB", "MAX", "MB", "OBJ", "C4D", "UNREAL", "USD"]


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
    category_id: int
    tags: List[str]
