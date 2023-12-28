import os
from typing import Dict, List
import logging
from smaug_cmd.adapter import fs
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.domain.upload_strategies import util
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class NormalResourceUploadStrategy(UploadStrategy):
    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        super().upload_textures(asset_template, user_id)
        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        text_key = ["texture", "tex", "texture_jpg"]
        group_files = group_files_by_directory(asset_template["textures"])
        filter_group_textures = util.filter_by_keywors(text_key, group_files)

        for t_key, files in filter_group_textures.items():
            # make texture zip file
            if len(files) == 0:
                continue
            zip_file_name = new_name = f"{asset_name}_{t_key}.zip"
            ziped_texture = fs.create_zip(files, zip_file_name)
            logger.info('Create "%s" Texture Zip: %s', t_key, ziped_texture)

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

    def upload_renders(self, asset_template: AssetTemplate, user_id: str):
        pass


def group_files_by_directory(files):
    """將檔案依照資料夾分組"""
    group_files: Dict[str, List[str]] = {}
    for f in files:
        dirname = os.path.dirname(f)
        if dirname not in group_files:
            group_files[dirname] = []
        group_files[dirname].append(f)

    new_group_files = {}
    for k, v in group_files.items():
        folder_name = os.path.basename(k)
        new_group_files[folder_name] = v
    return new_group_files
