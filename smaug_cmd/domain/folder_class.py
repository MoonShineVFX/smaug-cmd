from typing import Dict, Type, Optional
from smaug_cmd.domain.folder_parsing import (
    BaseFolder,
    AssetDepartModelFolder,
    NormalResourceModelFolder,
    AvalonResourceModelFolder,
    DownloadVariant1ResourceModelFolder,
    ThreedMaxResourceModelFolder,
    TaiwanCultureResourceModelFolder,
)
from smaug_cmd.domain.upload_strategies import (
    BaseUploadStrategy,
    AssetDepartUploadStrategy,
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._mapping: Dict[Type[BaseFolder], Type[BaseUploadStrategy]] = {
            AssetDepartModelFolder: AssetDepartUploadStrategy,
            TaiwanCultureResourceModelFolder: BaseUploadStrategy,
            NormalResourceModelFolder: BaseUploadStrategy,
            AvalonResourceModelFolder: BaseUploadStrategy,
            DownloadVariant1ResourceModelFolder: BaseUploadStrategy,
            ThreedMaxResourceModelFolder: BaseUploadStrategy,
        }

    def create(self) -> Optional[BaseFolder]:
        for cls in BaseFolder.__subclasses__():
            if cls.is_applicable(self._path):
                UploadStrategy = self._mapping[cls]
                return cls(self._path, UploadStrategy())
        return None
