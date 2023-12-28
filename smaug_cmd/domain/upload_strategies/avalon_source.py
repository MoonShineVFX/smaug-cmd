import logging
import os
from typing import Dict, List
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.domain.exceptions import SmaugApiError
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
        group_files = _group_files_by_directory(asset_template["textures"])
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
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": user_id,
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)


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


def _group_files_by_directory(files: List) -> Dict[str, List[str]]:
    """Group files by directory.

    :param files: A list of files.
    :return: A dict of files.
    """
    result: Dict[str, List[str]] = {}
    for file in files:
        dir_name = os.path.dirname(file)
        if dir_name not in result:
            result[dir_name] = []
        result[dir_name].append(file)
    return result


def exclude_key_from_dict(original_dict, key_to_exclude: str):
    return {k: v for k, v in original_dict.items() if key_to_exclude.find(k) == -1}
