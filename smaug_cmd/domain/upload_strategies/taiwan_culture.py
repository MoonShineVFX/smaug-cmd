import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.domain.upload_strategies import util
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class TaiwanCultureUploader(UploadStrategy):
    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        """上傳貼圖檔，提供基礎實作
        重新命名每個圖檔，並上傳至 OOS, 再建立資料庫資料連資料
        """
        # 執行基本檢查
        super().upload_textures(asset_template, user_id)

        # 取得必要 asset 資料
        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        # 整理貼圖檔案
        tex_key = ["textures", "texture_jpg"]
        group_textures = group_texture_files(tex_key, asset_template["textures"])

        # 建立資料庫資料
        for text_key, files in group_textures.items():
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
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)


def group_texture_files(tex_key, group_files):
    """將貼圖檔案分組, 並重新命名鍵值"""
    mapping = {
        "textures": "basic",
        "texture_jpg": "jpg",
    }
    re = {}
    group_files = util.filter_by_keywors(tex_key, group_files)
    for k, v in group_files.items():
        for keyword in tex_key:
            if k.find(keyword) != -1:
                re[mapping[keyword]] = v
                continue
    return re
