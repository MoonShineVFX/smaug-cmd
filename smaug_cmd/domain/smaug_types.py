from enum import Enum
from typing import Dict, Literal, TypedDict, List


class AssetTemplate(TypedDict):
    name: str
    previews: List[str]     # 預覽圖
    preview_model: str      # 預覽模型
    models: List[str]       # 模型
    textures: List[str]     # 貼圖
    meta: Dict[str, str]    # 其他資料(如果有)


class AssetFolderType(Enum):
    """Enum for the type of asset folder."""
    UNKNOWN = 0
    RESOURCE_DEPART = 1
    ASSET_DEPART = 2


RepresentationType = Literal["MODEL", "PREVIEW", "RENDER", "TEXTURE"]
RepresentationFormat = Literal["IMG", "FBX", "GLB", "MAX", "MB", "OBJ", "C4D", "UNREAL", "USD"]


class Representation(TypedDict):
    name: str
    type: RepresentationType
    format: RepresentationFormat
    path: str


class Asset(TypedDict):
    name: str
    categoryId: int
    representations: List[Representation]
    tags: List[str]