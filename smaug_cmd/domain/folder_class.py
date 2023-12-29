from typing import Dict, Type, Optional
from smaug_cmd.domain.folder_parsing import (
    BaseFolder,
    AssetDepartModelFolder,
    AvalonResourceFolder,
    TaiwanCultureResourceFolder,
    NormalResourceFolder,
    # DownloadVariant1Folder
    ThreedMaxResourceFolder
)
from smaug_cmd.domain.upload_strategies import (
    UploadStrategy,
    AssetDepartUploader,
    AvalonResourceUploader,
    TaiwanCultureUploader,
    NormalResourceUploader,
    # DownloadVariant1UploadStrategy,
    ThreeDMaxUploader
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._mapping: Dict[Type[BaseFolder], Type[UploadStrategy]] = {
            AssetDepartModelFolder: AssetDepartUploader,
            TaiwanCultureResourceFolder: TaiwanCultureUploader,
            AvalonResourceFolder: AvalonResourceUploader,
            NormalResourceFolder: NormalResourceUploader,
            # DownloadVariant1Folder: DownloadVariant1UploadStrategy
            ThreedMaxResourceFolder: ThreeDMaxUploader,
        }

    def create(self) -> Optional[BaseFolder]:
        for cls in BaseFolder.__subclasses__():
            if cls.is_applicable(self._path):
                UploadStrategy = self._mapping[cls]
                return cls(self._path, UploadStrategy())
        return None
