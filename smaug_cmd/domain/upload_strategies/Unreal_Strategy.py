import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.smaug_types import AssetTemplate, RepresentationCreateParams
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

from pprint import pprint

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class UnrealResourceUploader(UploadStrategy):
    def upload_previews(self, asset_template: AssetTemplate, user_id: str):
        # previews 就是 render
        pass

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        # UE 素材沒有材質 只有整包素材包
        pass

    def upload_renders(self, asset_template: AssetTemplate, upload_user: str):
        """硬拿 previews 當 render 上傳"""

        # yung add
        print ( '\n' )
        logger.info(">>>>> upload_renders")

        previews = asset_template["previews"]
        if len(previews) == 0:
            return
        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        for idx, render_file in enumerate(previews):
            
            # yung add
            # 因為是從 "_Pic" 去抓圖檔的路徑，還是先確認圖片存在，再做上傳動作比較保險 
            if os.path.exists(render_file):
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

    def upload_models(self, asset_template: AssetTemplate, upload_user: str):
        super().upload_models(asset_template, upload_user)

        # yung add
        print ( '\n' )
        logger.info(">>>>> upload_models")
        # pprint (asset_template)

        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]
        baseFolder = asset_template["basedir"]

        subfolders = [f.path for f in os.scandir(baseFolder) if f.is_dir()]

        # 篩選出UE的素材包路徑
        UEfolder = []
        noMatchSring = [
            ".smaug",
            "_RAR",
            "_Output",
            "_Backup",
            "_backup",
            "_Rar",
            "_rar",
        ]
        for folder in subfolders:
            if not any([x in folder for x in noMatchSring]):
                UEfolder.append(folder)

        logger.info("UEfolder: %s", UEfolder)

        if len(UEfolder) != 1:
            # 如果超過或少於一個UE素材包可以被壓縮，須進入路徑檢查
            logger.info("errorFolder: %s", baseFolder)
        else:
            zip_file_name = asset_name + "_" + UEfolder[0].split("/")[-1]
            ziped_Model = fs.create_zip_Folder(UEfolder, zip_file_name)
            logger.info("ziped_Model: %s", ziped_Model)

            # 確認壓縮檔存在，才執行上傳
            if not os.path.exists(ziped_Model):
                ziped_Model = ""
                logger.info("UEfolder has no zip file")
            else:
                # 上傳至 OOS
                upload_zip_object_name = rfs.put_representation1(
                    asset_id, zip_file_name, ziped_Model
                )

                # 把壓縮檔移至 .smaug 下
                # moved_zip_file = fs.collect_to_smaug( asset_template["basedir"], ziped_Model )

                RepresentationOp.create(
                    {
                        "assetId": asset_id,
                        "name": zip_file_name,
                        # check
                        "type": "GAME_ASSET",
                        "format": "UNREAL",
                        "usage": "DOWNLOAD",
                        # "fileSize": os.path.getsize(moved_zip_file),
                        "fileSize": os.path.getsize(ziped_Model),
                        "uploaderId": upload_user,
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


def exclude_key_from_dict(original_dict, key_to_exclude: str):
    return {k: v for k, v in original_dict.items() if key_to_exclude.find(k) == -1}
