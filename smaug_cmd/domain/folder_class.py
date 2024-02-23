from typing import Dict, Type, Optional
from smaug_cmd.domain.folder_parsing import (
    BaseFolder,
    AssetDepartModelFolder,
    AvalonResourceFolder,
    TaiwanCultureResourceFolder,
    NormalResourceFolder,
    UnrealResourceFolder,
    # DownloadVariant1Folder
    ThreedMaxResourceFolder,
    Kitbash3DResourceFolder
)
from smaug_cmd.domain.upload_strategies import (
    UploadStrategy,
    AssetDepartUploader,
    AvalonResourceUploader,
    TaiwanCultureUploader,
    NormalResourceUploader,
    UnrealResourceUploader,
    # DownloadVariant1UploadStrategy,
    ThreeDMaxUploader,
    Kitbash3DUploader
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path

        self._mapping: Dict[Type[BaseFolder], Type[UploadStrategy]] = {
            AssetDepartModelFolder: AssetDepartUploader,
            TaiwanCultureResourceFolder: TaiwanCultureUploader,
            AvalonResourceFolder: AvalonResourceUploader,
            NormalResourceFolder: NormalResourceUploader,
            UnrealResourceFolder: UnrealResourceUploader,
            # DownloadVariant1Folder: DownloadVariant1UploadStrategy
            ThreedMaxResourceFolder: ThreeDMaxUploader,
            Kitbash3DResourceFolder: Kitbash3DUploader,
        }

    def create(self) -> Optional[BaseFolder]:

        for cls in BaseFolder.__subclasses__():

            if cls.is_applicable(self._path):
                UploadStrategy = self._mapping[cls]

                print ( 'cls: ', cls )
                return cls( self._path, UploadStrategy() )
            
        return None
    
if __name__=='__main__':
    folder = "R:/_Asset/Game_Unreal/AncientEast/AsianTemple/"
    FolderClassFactory.create(folder)
