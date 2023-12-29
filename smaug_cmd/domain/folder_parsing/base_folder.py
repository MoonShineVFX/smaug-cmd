import datetime
import os
import logging
from typing import List, Optional
from smaug_cmd.adapter.smaug import SmaugJson
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.setting import (
    exclude_files,
    exclude_folders,
)
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.domain.upload_strategies.base_upload_strategy import BaseUploadStrategy
from smaug_cmd.domain.operators import AssetOp

logger = logging.getLogger("smaug_cmd.domain.folders")


class BaseFolder:
    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        """判斷 folderpath 是否是此類別能處理的資料夾"""
        raise NotImplementedError

    def __init__(
        self,
        path: str,
        upload_strategy: BaseUploadStrategy,
        asset_name: Optional[str] = None,
    ):
        self.upload_strategy = upload_strategy
        self._folder_type = FolderType.UNKNOWN
        self._path = path.replace("\\", "/")
        self._rawfilepaths: List[str] = []
        asset_name = ""
        if path and path[-1] == "/":
            asset_name = path.split("/")[-2]
        else:
            asset_name = os.path.basename(path)

        self._at: AssetTemplate = {
            "id": None,
            "name": asset_name,
            "categoryId": None,
            "previews": [],  # 預覽圖
            "preview_model": "",  # 預覽模型
            "models": [],  # 模型
            "textures": [],  # 貼圖
            "renders": [],  # 渲染圖
            "meta": {},  # 其他資料(如果有)
            "tags": [],  # 標籤
            "basedir": self._path,  # 資料夾路徑
            "createAt": None,
            "updateAt": None,
            "folderType": self._folder_type.value,
        }
        self._parsing()
        self._init_from_smaug()
        if asset_name is not None:
            self._at["name"] = asset_name

    def _parsing(self):
        # 取得資料夾的所有內容檔案
        for root, folders, files in os.walk(self._path):
            if os.path.basename(root) in exclude_folders:
                continue
            for file in files:
                if file in exclude_files:
                    continue
                self._rawfilepaths.append(os.path.join(root, file).replace("\\", "/"))
                file_path = os.path.join(root, file).replace("\\", "/")
                if self.is_texture(file_path):
                    self._at["textures"].append(file_path)
                elif self.is_preview(file_path):
                    self._at["previews"].append(file_path)
                elif self.is_render_image(file_path):
                    self._at["renders"].append(file_path)
                elif self.is_model(file_path):
                    self._at["models"].append(file_path)
                else:
                    logger.debug("drop file : %s", file_path)

            for file in self._at["models"]:
                if self.is_3d_preview(file):
                    self._at["preview_model"] = file
                    self._at["models"].remove(file)
                    break

    def is_preview(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_render_image(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_model(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_texture(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_3d_preview(self, file_path: str) -> bool:
        """預設的 3d 預覽檔案判斷
        檔名以 "_preview.glb" 結束
        """
        if file_path.endswith("_preview.glb"):
            return True
        return False

    def _init_from_smaug(self):
        """從 smaug.json 資料夾中讀取資料"""
        if not os.path.exists(self._path + "/.smaug"):
            return
        sjosn = SmaugJson(self._path)
        data = sjosn.deserialize()
        self._at.update(data)

    def asset_template(self) -> AssetTemplate:
        return self._at

    def folder_type(self) -> FolderType:
        return self._folder_type

    def upload_asset(self, asset_template, uploader_id: str):
        """上傳模板"""
        assert_resp = AssetOp.create(asset_template)
        logger.info("Asset: %s Created", asset_template["name"])
        asset_id = assert_resp["id"]
        self._at["id"] = asset_id
        asset_template["id"] = asset_id
        asset_name = asset_template["name"]

        logger.info("Asset %s: preview Uploading", asset_name)
        try:
            self.upload_strategy.upload_previews(asset_template, uploader_id)
        except SmaugApiError as e:
            logger.warning("Failed to upload previews. Reason: %s", e)

        logger.info("Asset %s: texture Uploading", asset_name)
        try:
            self.upload_strategy.upload_textures(asset_template, uploader_id)
        except SmaugApiError as e:
            logger.warning("Failed to upload textures. Reason: %s", e)

        logger.info("Asset %s: render Uploading", asset_name)
        try:
            self.upload_strategy.upload_renders(asset_template, uploader_id)
        except SmaugApiError as e:
            logger.warning("Failed to upload renders. Reason: %s", e)

        logger.info("Asset %s: model Uploading", asset_name)
        try:
            self.upload_strategy.upload_models(asset_template, uploader_id)
        except SmaugApiError as e:
            logger.warning("Failed to upload models. Reason: %s", e)

        logger.info("Asset %s: 3d preview Uploading", asset_name)
        try:
            self.upload_strategy.upload_3d_preview(asset_template, uploader_id)
        except SmaugApiError as e:
            logger.warning("Failed to upload 3d preview. Reason: %s", e)

        # write asset id to smaug.hson
        sm_json = SmaugJson(asset_template["basedir"])
        sm_json["id"] = asset_id
        sm_json["createAt"] = assert_resp["createAt"]
        sm_json["folderType"] = asset_template["folderType"]
        if assert_resp["updateAt"]:
            sm_json["updateAt"] = assert_resp["updateAt"]

        sm_json.serialize()
        logger.info("Write info to .smaug")
        logger.info("Asset: %s(%s) Upload is Done", asset_name, asset_id)
