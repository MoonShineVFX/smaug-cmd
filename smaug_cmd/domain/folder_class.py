import os
from typing import List

from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain.smaug_types import (
    AssetFolderType,
    AssetTemplate,
    ResourceFolderType,
)
from smaug_cmd.setting import exclude_files, exclude_folders


class FolderClassFactory:
    def __init__(self, path: str):
        self._path = path
        self._folder_type = self._which_folder_type()
        self._mapping = {
            ResourceFolderType.NORMAL_RESOURCE_MODEL: NormalResourceModelFolder,
            ResourceFolderType.AVALON_SOURCE_MODEL: AvalonResourceModelFolder,
            ResourceFolderType.DOWNLOAD_VARIANT1_MODEL: DownloadVariant1ResourceModelFolder,
            ResourceFolderType.DOWNLOAD_VARIANT2_MODEL: DownloadVariant2ResourceModelFolder,
            ResourceFolderType.THREE_MAX_MODEL: ThreedMaxResourceModelFolder,
        }

    def _which_folder_type(self):
        if ps.is_asset_depart_folder(self._path):
            return AssetFolderType.ASSET_DEPART
        elif ps.is_resource_depart_folder(self._path):
            return AssetFolderType.RESOURCE_DEPART
        elif ps.is_download_variant1_folder(self._path):
            return ResourceFolderType.DOWNLOAD_VARIANT1_MODEL
        elif ps.is_download_variant2_folder(self._path):
            return ResourceFolderType.DOWNLOAD_VARIANT2_MODEL
        elif ps.is_3dsmax_folder(self._path):
            return ResourceFolderType.THREE_MAX_MODEL
        else:
            raise SmaugApiError("Unknown folder type")

    def create(self):
        return self._mapping[self._folder_type](self._path)


class BaseFolder:
    def __init__(self, path: str):
        self._rawfilepaths: List[str] = []
        self._at: AssetTemplate = {
            "id": None,
            "name": "",
            "categoryId": None,
            "previews": [],
            "preview_model": "",
            "models": [],
            "textures": [],
            "renders": [],
            "meta": {},
            "tags": [],
            "basedir": "",
            "createAt": None,
            "updateAt": None,
        }
        self._at["name"] = os.path.basename(path)
        self._at["basedir"] = path
        self._collect_previews()
        self._collect_renders()
        self._collect_models()
        self._collect_textures()
        self._collect_tags()
        self._collect_meta()

    def _init(self):
        # 取得資料夾的所有內容檔案
        for root, folders, files in os.walk(self._at["basedir"]):
            if os.path.basename(root) in exclude_folders:
                continue
            for file in files:
                if file in exclude_files:
                    continue
                self._rawfilepaths.append(os.path.join(root, file))

    def _collect_previews(self):
        raise NotImplementedError

    def _collect_models(self):
        raise NotImplementedError

    def _collect_textures(self):
        raise NotImplementedError

    def _collect_renders(self):
        raise NotImplementedError

    def _collect_tags(self):
        raise NotImplementedError

    def _collect_meta(self):
        raise NotImplementedError

    def assetTemplate(self):
        return self._at
