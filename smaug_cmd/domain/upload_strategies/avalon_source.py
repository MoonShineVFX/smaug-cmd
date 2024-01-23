import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.upload_strategies import util
from smaug_cmd.domain.smaug_types import AssetTemplate, RepresentationCreateParams
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class AvalonResourceUploader(UploadStrategy):
    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        # 執行基本檢查
        super().upload_textures(asset_template, user_id)

        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        keyword_group = ["_AvalonSource/texture", "_AvalonSource/texture_low"]
        group_files = util.group_files_by_directory(asset_template["textures"])
        filter_group_files = _filter_by_keywors(keyword_group, group_files)
        texture_groups = {os.path.basename(k): v for k, v in filter_group_files.items()}
        for text_key, files in texture_groups.items():
            # make texture zip file
            if len(files) == 0:
                continue
            zip_file_name = new_name = f"{asset_name}_{text_key}.zip"
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
                    "usage": "DOWNLOAD",
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)

    def upload_renders(self, asset_template: AssetTemplate, upload_user: str):
        """硬拿 previews 當 render 上傳"""
        previews = asset_template["previews"]
        if len(previews) == 0:
            return
        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        for idx, render_file in enumerate(previews):
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



def _filter_by_keywors(keyword_group, group_files):
    filter_group_files = {}
    for k, v in group_files.items():
        for keyeord in keyword_group:
            if k.find(keyeord) != -1:
                filter_group_files[k] = v
                continue
    return filter_group_files


# import os
# from pprint import pprint
# for root, _, files in os.walk(r"Y:\resource\_Asset\MoonshineProject_2019_Obsidian\201903_Jdb\Prop\Bag"):
#     for file in files:
#         pprint(os.path.join(root, file).replace("\\", "/"))


def exclude_key_from_dict(original_dict, key_to_exclude: str):
    return {k: v for k, v in original_dict.items() if key_to_exclude.find(k) == -1}
