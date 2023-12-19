from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain import parsing as ps


from smaug_cmd.domain.folder_parsing import (
    FolderType,
    AssetFolderType,
    NormalResourceModelFolder,
    AvalonResourceModelFolder,
    DownloadVariant1ResourceModelFolder,
    ThreedMaxResourceModelFolder,
    TaiwanCultureResourceModelFolder,
    is_taiwan_culture_model_folder,
    is_avalon_source_model_folder,
    is_normal_resource_model_folder,
    is_download_variant1_model_folder,
    is_3dmax_model_folder,
)


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._folder_type = self._which_folder_type()
        self._mapping = {
            FolderType.TAIWAN_CULTURE_MODEL: TaiwanCultureResourceModelFolder,
            FolderType.NORMAL_RESOURCE_MODEL: NormalResourceModelFolder,
            FolderType.AVALON_SOURCE_MODEL: AvalonResourceModelFolder,
            FolderType.DOWNLOAD_VARIANT1_MODEL: DownloadVariant1ResourceModelFolder,
            FolderType.THREE_MAX_MODEL: ThreedMaxResourceModelFolder,
        }

    def _which_folder_type(self):
        if ps.is_asset_depart_folder(self._path):
            return AssetFolderType.ASSET_DEPART
        elif is_taiwan_culture_model_folder(self._path):
            return FolderType.TAIWAN_CULTURE_MODEL
        elif is_avalon_source_model_folder(self._path):
            return FolderType.AVALON_SOURCE_MODEL
        elif is_download_variant1_model_folder(self._path):
            return FolderType.DOWNLOAD_VARIANT1_MODEL
        elif is_3dmax_model_folder(self._path):
            return FolderType.THREE_MAX_MODEL
        else:
            raise SmaugApiError("Unknown folder type")

    def create(self):
        return self._mapping[self._folder_type](self._path)
