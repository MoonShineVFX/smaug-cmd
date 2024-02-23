import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.smaug_types import AssetTemplate, RepresentationCreateParams
from smaug_cmd.domain.upload_strategies import util
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class Kitbash3DUploader(UploadStrategy):
    def upload_previews(self, asset_template: AssetTemplate, user_id: str):
        thumb =''
        thumbList = []        
        baseFolder = asset_template["basedir"]
        for preview in  asset_template['previews']:
            if '_thumbnail' in preview:
                thumb = preview
                thumbList.append(thumb)
            else:
                if '_All' not in preview:
                    thumb = preview
                    print (  )

        # Yung add
        print ( "Get thumb: ", thumb )
        if not os.path.exists(thumb): 
            print ( 'error >> render_file not exist' )
            thumb = baseFolder + '/' +  os.path.basename(thumb)
            print ( 'render_file: ', thumb )

        if len(thumbList) == 0:
            print ( 'error >> no thumbnail: ', baseFolder )

        super()._upload_thumbnail(asset_template, user_id, thumb)

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        """上傳貼圖檔，提供基礎實作
        重新命名每個圖檔，並上傳至 OOS, 再建立資料庫資料連資料
        """

        # yung add
        # 跳過材質上傳 
        pass


        # # 執行基本檢查
        # super().upload_textures(asset_template, user_id)

        # # 取得必要 asset 資料
        # asset_id = asset_template["id"]
        # assert asset_id is not None, "Asset id is None"
        # asset_name = asset_template["name"]

        # # 整理貼圖檔案
        # tex_key = ["textures", "texture_jpg"]
        # group_textures = group_texture_files(tex_key, asset_template["textures"])

        # # 建立資料庫資料
        # for text_key, files in group_textures.items():
        #     # make texture zip file
        #     if len(files) == 0:
        #         continue
        #     zip_file_name = new_name = f"{asset_name}_{text_key}.zip"
        #     ziped_texture = fs.create_zip(files, zip_file_name)
        #     logger.info('Create "%s" Texture Zip: %s', text_key, ziped_texture)

        #     # 上傳至 OOS
        #     upload_zip_object_name = rfs.put_representation1(
        #         asset_id, new_name, ziped_texture
        #     )
        #     # 把 ziped_texture 移至 .smaug 下
        #     moved_zip_file = fs.collect_to_smaug(
        #         asset_template["basedir"], ziped_texture
        #     )

        #     RepresentationOp.create(
        #         {
        #             "assetId": asset_id,
        #             "name": zip_file_name,
        #             "type": "TEXTURE",
        #             "format": "IMG",
        #             "usage": "DOWNLOAD",
        #             "fileSize": os.path.getsize(moved_zip_file),
        #             "uploaderId": user_id,
        #             "path": upload_zip_object_name,
        #             "meta": {},
        #         }
        #     )
        #     logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)


    def group_texture_files(tex_key, group_files):
        # yung add
        # 跳過貼圖上傳
        pass

        # """將貼圖檔案分組, 並重新命名鍵值"""
        # mapping = {
        #     "textures": "basic",
        #     "texture_jpg": "jpg",
        # }
        # re = {}
        # group_files = util.filter_by_keywors(tex_key, group_files)
        # for k, v in group_files.items():
        #     for keyword in tex_key:
        #         if k.find(keyword) != -1:
        #             re[mapping[keyword]] = v
        #             continue
        # return re
    
    def upload_renders(self, asset_template: AssetTemplate, upload_user: str):
        """硬拿 previews 當 render 上傳"""

        # yung add
        print ( '\n' )
        logger.info(">>>>> upload_renders")
        # pprint ( asset_template )

        previews = asset_template["previews"]
        if len(previews) == 0:
            return
        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        for idx, render_file in enumerate(previews):
            
            # yung add
            baseFolder = asset_template["basedir"]

            file_extension = os.path.splitext(render_file)[-1].lower()
            file_name = f"render-{idx}{file_extension}"
            new_name = f"{asset_name}_{file_name}"

            # 如果路徑不存在去素材資料夾找 圖片在資料夾一定會有
            if not os.path.exists(render_file):
                print ( 'error >> render_file not exist' )
                render_file = baseFolder + '/' +  os.path.basename(render_file)
                print ( 'render_file: ', render_file )

            # 因為是從 "_Pic" 去抓圖檔的路徑，還是先確認圖片存在，再做上傳動作比較保險 
            if os.path.exists(render_file):
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
        # super().upload_models(asset_template, upload_user)

        # yung add
        print ( '\n' )
        logger.info(">>>>> upload_models, no model, pass")
        # pprint (asset_template)

        # asset_id = asset_template["id"]
        # assert asset_id is not None, "Asset id is None"
        # asset_name = asset_template["name"]
        # baseFolder = asset_template["basedir"]

        # subfolders = [f.path for f in os.scandir(baseFolder) if f.is_dir()]

        # # 篩選出UE的素材包路徑
        # TWfolder = []
        # noMatchSring = [
        #     ".smaug",
        #     "_RAR",
        #     "_Output",
        #     "_Backup",
        #     "_backup",
        #     "_Rar",
        #     "_rar",
        # ]
        # for folder in subfolders:
        #     if not any([x in folder for x in noMatchSring]):
        #         folder = folder.replace("\\", "/")
        #         TWfolder.append(folder)

        # logger.info("TWfolder: %s", TWfolder)

        # if len(TWfolder) != 1:
        #     # 如果超過或少於一個UE素材包可以被壓縮，須進入路徑檢查
        #     logger.info("errorFolder: %s", baseFolder)
        # else:
        #     zip_file_name = asset_name + "_" + TWfolder[0].split("/")[-1]
        #     ziped_Model = fs.create_zip_Folder(TWfolder, zip_file_name)
        #     logger.info("ziped_Model: %s", ziped_Model)

        #     # 確認壓縮檔存在，才執行上傳
        #     if not os.path.exists(ziped_Model):
        #         ziped_Model = ""
        #         logger.info("TWfolder has no zip file")
        #     else:
        #         # 上傳至 OOS
        #         upload_zip_object_name = rfs.put_representation1(
        #             asset_id, zip_file_name, ziped_Model
        #         )

        #         # 把壓縮檔移至 .smaug 下
        #         # moved_zip_file = fs.collect_to_smaug( asset_template["basedir"], ziped_Model )

        #         RepresentationOp.create(
        #             {
        #                 "assetId": asset_id,
        #                 "name": zip_file_name,
        #                 # check
        #                 "type": "MODEL",
        #                 "format": "FBX",
        #                 "usage": "DOWNLOAD",
        #                 # "fileSize": os.path.getsize(moved_zip_file),
        #                 "fileSize": os.path.getsize(ziped_Model),
        #                 "uploaderId": upload_user,
        #                 "path": upload_zip_object_name,
        #                 "meta": {},
        #             }
        #         )
        #         logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)
