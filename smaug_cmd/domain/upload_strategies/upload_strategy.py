import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain.smaug_types import AssetTemplate, RepresentationCreateParams
from smaug_cmd.domain.upload_strategies.base_upload_strategy import BaseUploadStrategy
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class UploadStrategy(BaseUploadStrategy):
    """上傳策略，提供基礎實作
    preview 的第一張圖會被當作 thumbnail 用途"""

    def upload_previews(self, asset_template: AssetTemplate, user_id: str):
        """上傳預覽圖，提供基礎實作
        重新命名每個圖檔，並上傳至 OOS, 再建立資料庫資料連資料
        """
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")

        if not asset_template["previews"]:
            raise SmaugApiError("Asset previews is empty")

        self._upload_thumbnail(asset_template, user_id, asset_template["previews"][0])

    def upload_renders(self, asset_template: AssetTemplate, upload_user: str):
        """上傳算圖檔，提供基礎實作
        重新命名每個圖檔，並上傳至 OOS, 再建立資料庫資料連資料
        """
        # 上傳 render 檔案
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")
        asset_name = asset_template["name"]
        for idx, render_file in enumerate(asset_template["renders"]):
            file_extension = os.path.splitext(render_file)[-1].lower()
            file_name = f"render-{idx}{file_extension}"
            new_name = f"{asset_name}_{file_name}"

            # 上傳到 SSO. 這樣才能拿到 id 寫至 db
            upload_object_name = rfs.put_representation1(
                asset_id, new_name, render_file
            )
            logger.debug(
                "Upload render files %s: %s as %s",
                asset_template["name"],
                render_file,
                new_name,
            )

            # 建立資料庫資料
            render_representation_create_payload: RepresentationCreateParams = {
                "assetId": asset_id,
                "name": new_name,
                "type": "RENDER",
                "format": "IMG",
                "usage": "PREVIEW",
                "fileSize": os.path.getsize(render_file),
                "uploaderId": upload_user,
                "path": upload_object_name,
                "meta": {},
            }
            RepresentationOp.create(render_representation_create_payload)
            logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

    def upload_models(self, asset_template: AssetTemplate, user_id: str):
        """上傳模型檔案，提供基礎實作
        依 DCC 軟體分類，並上傳至 OOS, 再建立資料庫資料連資料
        """
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")

        asset_name = asset_template["name"]
        model_groups = ps.model_group(asset_template["models"])
        for model_key, files in model_groups.items():
            if len(files) == 0:
                continue
            # make model zip payload
            zip_file_name = new_name = f"{asset_name}_{model_key}_models.zip"
            ziped_model = fs.create_zip(files, zip_file_name)
            logger.debug(f'Create "{model_key}" Model Zip')
            # 準備上傳至 OOS
            upload_model_object_name = rfs.put_representation1(
                asset_id, new_name, ziped_model
            )
            # 把 ziped_model 移至 .smaug 下
            moved_zip_file = fs.collect_to_smaug(asset_template["basedir"], ziped_model)

            pre_format = ps.format_from_softkey(model_key)
            RepresentationOp.create(
                {
                    "assetId": asset_id,
                    "name": zip_file_name,
                    "type": "MODEL",
                    "format": pre_format,
                    "usage": "DOWNLOAD",
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_model_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        """上傳貼圖檔案
        這個方法會把貼圖檔案分類，並上傳至 OOS, 再建立資料庫資料連資料
        怎麼分類就依子類別實作
        """
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")
        if not asset_template["textures"]:
            raise SmaugApiError("Asset textures is empty")

    def upload_3d_preview(self, asset_template: AssetTemplate, user_id):
        """上傳 3D 預覽檔案, 提供基礎實作"""
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")
        if not asset_template["preview_model"]:
            raise SmaugApiError("Asset preview model is empty")

        asset_name = asset_template["name"]
        preview_glb = asset_template["preview_model"]
        logger.debug("Found preview model: %s", preview_glb)

        preview_glb_name = f"{asset_name}_preview.glb"
        upload_preview_glb_object_name = rfs.put_representation1(
            asset_id, preview_glb_name, preview_glb
        )
        RepresentationOp.create(
            {
                "assetId": asset_id,
                "name": preview_glb_name,
                "type": "MODEL",
                "format": "GLB",
                "usage": "PREVIEW",
                "fileSize": os.path.getsize(preview_glb),
                "uploaderId": user_id,
                "path": upload_preview_glb_object_name,
                "meta": {},
            }
        )
        logger.debug("Create DB record for Asset(%s): %s", asset_id, preview_glb_name)

    def _upload_pic(self, asset_template, user_id, idx, preview_file):
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")

        # 重新命名檔案
        asset_name = asset_template["name"]
        file_extension = os.path.splitext(preview_file)[-1].lower()
        if idx:
            file_name = f"preview-{idx}{file_extension}"
        else:
            file_name = f"preview{file_extension}"
        new_name = f"{asset_name}_{file_name}"

        # 上傳至 OOS，這樣才能拿到 id 寫至 db
        upload_object_name = rfs.put_representation1(asset_id, new_name, preview_file)

        logger.debug(
            "Upload Asset(%s)previes files: %s as %s",
            asset_template["name"],
            preview_file,
            new_name,
        )

        # 建立資料庫資料
        preview_create_represent_payload: RepresentationCreateParams = {
            "assetId": asset_id,
            "name": new_name,
            "type": "RENDER",
            "format": "IMG",
            "usage": "PREVIEW",
            "fileSize": os.path.getsize(preview_file),
            "uploaderId": user_id,
            "path": upload_object_name,
            "meta": {},
        }
        RepresentationOp.create(preview_create_represent_payload)
        logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

    def _upload_thumbnail(self, asset_template, user_id, preview_file):
        asset_id = asset_template["id"]
        if asset_id is None:
            raise SmaugApiError("Asset id is None")

        # 重新命名檔案
        asset_name = asset_template["name"]
        file_extension = os.path.splitext(preview_file)[-1].lower()

        file_name = f"thumb-{file_extension}"
        new_name = f"{asset_name}_{file_name}"

        # 上傳至 OOS，這樣才能拿到 id 寫至 db
        upload_object_name = rfs.put_representation1(asset_id, new_name, preview_file)

        logger.debug(
            "Upload Asset(%s)previes files: %s as %s",
            asset_template["name"],
            preview_file,
            new_name,
        )

        # 建立資料庫資料
        preview_create_represent_payload: RepresentationCreateParams = {
            "assetId": asset_id,
            "name": new_name,
            "type": "RENDER",
            "format": "IMG",
            "usage": "THUMBNAIL",
            "fileSize": os.path.getsize(preview_file),
            "uploaderId": user_id,
            "path": upload_object_name,
            "meta": {},
        }
        RepresentationOp.create(preview_create_represent_payload)
        logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)
