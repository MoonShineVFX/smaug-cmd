from typing import List, Type
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.folder_parsing import (
    BaseFolder,
    AssetDepartModelFolder,
    NormalResourceModelFolder,
    AvalonResourceModelFolder,
    DownloadVariant1ResourceModelFolder,
    ThreedMaxResourceModelFolder,
    TaiwanCultureResourceModelFolder,
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._mapping: List[Type[BaseFolder]] = [
            AssetDepartModelFolder,
            TaiwanCultureResourceModelFolder,
            NormalResourceModelFolder,
            AvalonResourceModelFolder,
            DownloadVariant1ResourceModelFolder,
            ThreedMaxResourceModelFolder,
        ]

    def create(self) -> BaseFolder:
        for FolderClass in self._mapping:
            folder_obj = FolderClass.create_if_applicable(self._path)
            if folder_obj is not None:
                return folder_obj
        raise SmaugApiError(f"無法判斷 {self._path} 的資料夾類型")