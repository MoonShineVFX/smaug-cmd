import logging
from typing import cast, List, Optional, Tuple, Callable
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QPushButton

from smaug_cmd.adapter.cmd_handlers.zip import create_zip
from smaug_cmd.domain.smaug_types import (
    Menu,
    MenuTree,
    AssetFolderType,
    AssetTemplate,
    AssetCreateResponse,
    AssetCreateParams,
    RepresentationCreateParams,
    RepresentationCreateResponse,
    UserInfo
)
from smaug_cmd.model import login_in as api_login, log_out as api_logout
from smaug_cmd.model import data as ds
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain import command as cmd
from smaug_cmd.domain.exceptions import SmaugError, SmaugOperaterError
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug-cmd.domain")



class SmaugCmdLogic(QObject):
    def __init__(self):
        super().__init__(None)
        self._current_user: Optional[UserInfo] = None

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb(error_msg) if er_cb else None

    def log_in(self, user_name, password) -> bool:
        user = api_login(user_name, password)
        self._current_user = user
        return True

    def get_menus(self, error_cb: Optional[Callable]) -> Optional[List[Menu]]:
        re = ds.get_menus()
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def get_menu_tree(
        self, menu_id, error_cb: Optional[Callable] = None
    ) -> Optional[MenuTree]:
        re = ds.get_menu_tree(menu_id)
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def cate_breadcrumb(
        self, cate: int, cate_lbl: QLabel, cate_picker_btn: QPushButton
    ):
        """組合麵包屑"""
        # 取的分類的父分類
        cate_query = ds.get_category(cate, force=True)
        if str(cate_query[0])[0] != "2":
            self.error_handler(cate_query[1]["message"])
            return
        cate_detail = cate_query[1]

        # 設定 UI
        cate_lbl.setText(f"category: {cate_detail['breadCrumb']}")
        cate_picker_btn.setProperty("smaug_cate", True)
        return

    def asset_template(self, folder_path) -> Optional[AssetTemplate]:
        # convert folder to asset template
        if ps.is_asset_model_folder(folder_path) == AssetFolderType.UNKNOWN:
            return None

        asset_template = ps.folder_asset_template(folder_path)
        # FileUtils.create_hidden_folder(asset_template["basedir"] + "/.smaug")
        return asset_template

    def create_asset_proc(self, asset_template: AssetTemplate):
        """在資料庫建立 asset 的流程
        建立 asset 以取得 asset id 後
        會處理模型檔跟貼圖檔的分類之後壓縮成 zip 檔案
        各別上傳完 zip 檔之後再去資料庫建立 representation
        """
        # 檢查是否登入
        if self._current_user is None:
            raise SmaugError("Please login first.")

        # 建立 asset 以取得 asset id
        assert_resp = AssetOp.create(asset_template)
        asset_id = assert_resp["id"]
        asset_name = asset_template["name"]
        logger.debug("Asset: %s(%s) Created", asset_name, asset_id)

        # 先上傳 preview 檔案
        for idx, preview_file in enumerate(asset_template["previews"]):
            # 重新命名檔案
            file_extension = os.path.splitext(preview_file)[-1].lower()
            file_name = f"preview-{idx}{file_extension}"
            object_name = f"{asset_name}_{file_name}"

            # 上傳至 OOS，這樣才能拿到 id 寫至 db
            upload_object_name = rfs.put_representation1(
                asset_id, preview_file, object_name
            )

            logger.debug(
                "Upload previes files %s: %s as %s",
                asset_template["name"],
                preview_file,
                object_name,
            )

            # 建立資料庫資料
            preview_create_represent_payload: RepresentationCreateParams = {
                "assetId": asset_id,
                "name": object_name,
                "type": "PREVIEW",
                "format": "IMG",
                "fileSize": os.path.getsize(preview_file),
                "uploaderId": self._current_user["id"],
                "path": upload_object_name,
                "meta": {},
            }
            RepresentationOp.create(preview_create_represent_payload)
            logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

        # 上傳 render 檔案
        for idx, render_file in enumerate(asset_template["renders"]):
            file_extension = os.path.splitext(preview_file)[-1].lower()
            file_name = f"render-{idx}{file_extension}"
            new_name = f"{asset_name}_{file_name}"

            # 上傳到 SSO. 這樣才能拿到 id 寫至 db
            upload_object_name = rfs.put_representation1(
                asset_id, render_file, new_name
            )
            logger.debug(
                "Upload render files %s: %s as %s",
                asset_template["name"],
                render_file,
                object_name,
            )

            # 建立資料庫資料
            render_representation_create_payload: RepresentationCreateParams = {
                "assetId": asset_id,
                "name": new_name,
                "type": "RENDER",
                "format": "IMG",
                "fileSize": os.path.getsize(render_file),
                "uploaderId": self._current_user["id"],
                "path": upload_object_name,
                "meta": {},
            }
            RepresentationOp.create(render_representation_create_payload)
            logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

        # 上傳 texture 檔案
        # splite textures to texture-group,
        
        texture_groups = ps.texture_group(asset_template["textures"])
        for text_key, files in texture_groups.items():
            # make texture zip file
            zip_file_name = object_name = f"{asset_name}_{text_key}_textures.zip"
            ziped_texture = create_zip(files, zip_file_name)
            logger.debug(f'Create "{text_key}" Texture Zip')

            # 準備上傳至 OOS
            upload_zip_object_name = rfs.put_representation1(asset_id, ziped_texture, object_name)

            RepresentationOp.create(
                {
                    "assetId": asset_id,
                    "name": zip_file_name,
                    "type": "TEXTURE",
                    "format": "IMG",
                    "fileSize": os.path.getsize(ziped_texture),
                    "uploaderId": self._current_user["id"],
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)
        
        # splite models to model-group
        model_groups = ps.model_group(asset_id, asset_template["models"])
        for model_key, files in model_groups.items():
            # make model zip payload
            zip_file_name = object_name = f"{asset_name}_{model_key}_models.zip"
            zip_process_cmds.append(
                (cmd.CreateZip(files, zip_file_name), f'Create "{model_key}" Model Zip')
            )

        # ---------------------
        # upload preview model process
        # upload textures process
        # upload models process
        # upload renders process
        # update meta data, find bounding box, find texture size, find model size..., etc.
        # update tags


class AssetOp(QObject):
    @classmethod
    def create(cls, asset_template: AssetTemplate) -> AssetCreateResponse:
        if asset_template["categoryId"] is None:
            logger.error("Asset category id is None")
            raise SmaugOperaterError("Asset category id is None")
        param_payload: AssetCreateParams = {
            "name": asset_template["name"],
            "category_id": asset_template["categoryId"],
            "tags": asset_template["tags"],
        }
        re = ds.create_asset(param_payload)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]


class RepresentationOp(QObject):
    @classmethod
    def create(
        cls, payload: RepresentationCreateParams
    ) -> RepresentationCreateResponse:
        re = ds.create_representation(payload)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        if re[1] is None:
            logger.error("Create representation return None")
            raise SmaugOperaterError("Create representation return None")
        else:
            return re[1]
