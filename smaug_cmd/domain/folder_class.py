from typing import Dict, Type, Optional
from smaug_cmd.domain.folder_parsing import (
    BaseFolder,
    AssetDepartModelFolder,
    AvalonResourceFolder,
    TaiwanCultureResourceFolder,
    NormalResourceFolder,
    UnrealResourceFolder,
    # DownloadVariant1Folder
    ThreedMaxResourceFolder
)
from smaug_cmd.domain.upload_strategies import (
    UploadStrategy,
    AssetDepartUploader,
    AvalonResourceUploader,
    TaiwanCultureUploader,
    NormalResourceUploader,
    UnrealResourceUploader,
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
            UnrealResourceFolder: UnrealResourceUploader,
            # DownloadVariant1Folder: DownloadVariant1UploadStrategy
            ThreedMaxResourceFolder: ThreeDMaxUploader,
        }

        # yung add
        print ( 'self._path: ', self._path )
        # print ( 'self._mapping: ', self._mapping )

    def create(self) -> Optional[BaseFolder]:
        # from smaug_cmd.domain.folder_parsing import ( BaseFolder,

        # print ( 'self: ', self )
        for cls in BaseFolder.__subclasses__():

            # yung add  
            # cls 為 Key 值
            
            # cls :  <class 'smaug_cmd.domain.folder_parsing.Unreal_Parsing.UnrealResourceFolder'>

            if cls.is_applicable(self._path):
                
                #從 Key 抓到 Value
                print ( 'cls : ', str(cls)  )
                UploadStrategy = self._mapping[cls]
                # 從這邊開始跑 UnrealResourceFolder: UnrealResourceUploader 這兩個函式
        
                # Yung add
                #  { 鍵 Key: 值 Value }
                # 使用 [] 符號，傳入鍵(Key)的名稱
                # print ( 'UploadStrategy: ', UploadStrategy )
                # print ( 'cls( self._path, UploadStrategy(): ', cls( self._path, UploadStrategy() ) )

                return cls( self._path, UploadStrategy() )
            
        return None
    
if __name__=='__main__':
    folder = "R:/_Asset/Game_Unreal/AncientEast/AsianTemple/"
    FolderClassFactory.create(folder)
