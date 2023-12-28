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
    UploadStrategy,
    AssetDepartUploadStrategy,
    AvalonResourceUploader,
    TaiwanCultureUploadStrategy
    
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._mapping: Dict[Type[BaseFolder], Type[UploadStrategy]] = {
            AssetDepartModelFolder: AssetDepartUploadStrategy,
            TaiwanCultureResourceModelFolder: TaiwanCultureUploadStrategy,
            AvalonResourceModelFolder: AvalonResourceUploader
            # NormalResourceModelFolder: BaseUploadStrategy,
        }

    def create(self) -> Optional[BaseFolder]:
        for cls in BaseFolder.__subclasses__():
            if cls.is_applicable(self._path):
                UploadStrategy = self._mapping[cls]
                return cls(self._path, UploadStrategy())
        return None
