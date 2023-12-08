from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any


class Command:
    pass


@dataclass
class CreateZip(Command):
    file_paths: List[str]
    zip_file_name: str


@dataclass
class CreateAsset(Command):
    name: str
    categoryId: Optional[int]
    meta: Dict[str, Any]    # 其他資料(如果有)
    tags: List[str]         # 標籤


@dataclass
class DeleteAsset(Command):
    assetId: str


@dataclass
class CreateRepresentation(Command):
    assetId: str
    name: str
    type: str
    format: str
    fileSize: int
    uploaderId: str
    path: str
    meta: Dict[str, Union[str, int]]


# minio
@dataclass
class UploadFile(Command):
    asset_id: str
    file_path: str
    object_name: str


@dataclass
class RemoveRepresentation(Command):
    object_name: str
