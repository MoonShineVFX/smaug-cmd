import logging
import os
from smaug_cmd.domain.smaug_types import (
    AssetTemplate,
    RepresentationCreateParams,
)
from smaug_cmd.adapter import fs
from smaug_cmd.domain.upload_strategies import UploadStrategy
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain import parsing as ps
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class AssetDepartUploadStrategy(UploadStrategy):
    def upload_previews(self, asset_template: AssetTemplate, user_id: str):
        for idx, preview_file in enumerate(asset_template["previews"]):
            asset_id = asset_template["id"]
            if asset_id is None:
                raise ValueError("Asset id is None")

            # 重新命名檔案
            asset_name = asset_template["name"]
            file_extension = os.path.splitext(preview_file)[-1].lower()
            file_name = f"preview-{idx}{file_extension}"
            new_name = f"{asset_name}_{file_name}"

            # 上傳至 OOS，這樣才能拿到 id 寫至 db
            upload_object_name = rfs.put_representation1(
                asset_id, new_name, preview_file
            )

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
                "type": "PREVIEW",
                "format": "IMG",
                "fileSize": os.path.getsize(preview_file),
                "uploaderId": user_id,
                "path": upload_object_name,
                "meta": {},
            }
            RepresentationOp.create(preview_create_represent_payload)
            logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

    def upload_renders(self, asset_template: AssetTemplate, upload_user: str):
        # 上傳 render 檔案
        asset_id = asset_template["id"]
        if asset_id is None:
            raise ValueError("Asset id is None")
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
                "fileSize": os.path.getsize(render_file),
                "uploaderId": upload_user,
                "path": upload_object_name,
                "meta": {},
            }
            RepresentationOp.create(render_representation_create_payload)
            logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        texture_groups = ps.texture_group(asset_template["textures"])
        asset_id = asset_template["id"]
        if asset_id is None:
            raise ValueError("Asset id is None")
        asset_name = asset_template["name"]
        for text_key, files in texture_groups.items():
            # make texture zip file
            if len(files) == 0:
                continue
            zip_file_name = new_name = f"{asset_name}_{text_key}_textures.zip"
            ziped_texture = fs.create_zip(files, zip_file_name)
            logger.info('Create "%s" Texture Zip: %s', text_key, ziped_texture)

            # 上傳至 OOS
            upload_zip_object_name = rfs.put_representation1(
                asset_id, new_name, ziped_texture
            )

            # 把 ziped_texture 移至 .smaug 下
            moved_zip_file = fs.collect_to_smaug(
                asset_template["basedir"], ziped_texture
            )

            RepresentationOp.create(
                {
                    "assetId": asset_id,
                    "name": zip_file_name,
                    "type": "TEXTURE",
                    "format": "IMG",
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)

    def upload_models(self, asset_template: AssetTemplate, user_id: str):
        asset_id = asset_template["id"]
        if asset_id is None:
            raise ValueError("Asset id is None")

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
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_model_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)

    def upload_3d_preview(self, asset_template: AssetTemplate, user_id: str):
        asset_id = asset_template["id"]
        if asset_id is None:
            raise ValueError("Asset id is None")

        asset_name = asset_template["name"]
        preview_glb = asset_template["preview_model"]
        if preview_glb is None:
            logger.debug("No preview model found")
            return
        logger.debug("Found preview model: %s", preview_glb)

        preview_glb_name = f"{asset_name}_preview.glb"
        upload_preview_glb_object_name = rfs.put_representation1(
            asset_id, preview_glb_name, preview_glb
        )
        RepresentationOp.create(
            {
                "assetId": asset_id,
                "name": preview_glb_name,
                "type": "PREVIEW",
                "format": "GLB",
                "fileSize": os.path.getsize(preview_glb),
                "uploaderId": user_id,
                "path": upload_preview_glb_object_name,
                "meta": {},
            }
        )
        logger.debug("Create DB record for Asset(%s): %s", asset_id, preview_glb_name)
