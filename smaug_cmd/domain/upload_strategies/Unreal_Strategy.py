import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.operators import RepresentationOp
from smaug_cmd.domain.upload_strategies import util
from smaug_cmd.domain.smaug_types import AssetTemplate, RepresentationCreateParams
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

import json

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class UnrealResourceUploader(UploadStrategy):

    def upload_previews(self, asset_template: AssetTemplate, user_id: str):
        pass

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        # 執行基本檢查
        # UE 素材沒有材質 只有整包素材包
        pass
        # super().upload_textures(asset_template, user_id)

        # asset_id = asset_template["id"]
        # assert asset_id is not None, "Asset id is None"
        # asset_name = asset_template["name"]

        # keyword_group = ["_AvalonSource/texture", "_AvalonSource/texture_low"]
        # group_files = util.group_files_by_directory(asset_template["textures"])
        # filter_group_files = _filter_by_keywors(keyword_group, group_files)
        # texture_groups = {os.path.basename(k): v for k, v in filter_group_files.items()}
        # for text_key, files in texture_groups.items():
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
        #             "fileSize": os.path.getsize(moved_zip_file),
        #             "uploaderId": user_id,
        #             "path": upload_zip_object_name,
        #             "meta": {},
        #         }
        #     )
        #     logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)

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

            # Yung add
            print ( 'idx: ', idx )
            print ( 'render_file: ', render_file )
            print ( 'file_extension: ', file_extension )
            print ( 'file_name: ', file_name )
            print ( 'new_name: ', new_name )
            print ( '\n' )


            # # 上傳到 SSO. 這樣才能拿到 id 寫至 db
            # upload_object_name = rfs.put_representation1(
            #     asset_id, new_name, render_file
            # )
            # logger.debug(
            #     "Upload render files %s: %s as %s",
            #     asset_template["name"],
            #     render_file,
            #     new_name,
            # )

            # # 建立資料庫資料
            # render_representation_create_payload: RepresentationCreateParams = {
            #     "assetId": asset_id,
            #     "name": new_name,
            #     "type": "RENDER",
            #     "format": "IMG",
            #     "fileSize": os.path.getsize(render_file),
            #     "uploaderId": upload_user,
            #     "path": upload_object_name,
            #     "meta": {},
            # }
            # RepresentationOp.create(render_representation_create_payload)
            # logger.debug("Create DB record for Asset(%s): %s", asset_id, file_name)

    def upload_models(self, asset_template: AssetTemplate, upload_user: str):
        super().upload_models(asset_template, upload_user)

        asset_id = asset_template["id"]
        assert asset_id is not None, "Asset id is None"
        asset_name = asset_template["name"]

        # yung add
        print ( 'asset_id: ', asset_id )
        print ( 'asset_name: ', asset_name )
        print ( '>>>> asset_template:', json.dumps(asset_template, indent=4, ensure_ascii=False)  )

        baseFolder = asset_template["basedir"]
        print ( 'baseFolder: ', baseFolder )

        subfolders = [ f.path for f in os.scandir(baseFolder) if f.is_dir() ]
        print ( 'subfolders: ', subfolders )
        

        UEfolder = []
        noMatchSring = [ '.smaug', '_RAR', '_Output' ]
        for folder in subfolders:
            if not any([x in folder for x in noMatchSring]):
                UEfolder.append(folder)

        print ( 'UEfolder: ', UEfolder )

        if len(UEfolder) == 1:
            print ( 'UEfolder[0]: ', UEfolder[0] )

            zip_file_name = asset_name + '_' + UEfolder[0].split('/')[-1] + '.zip'
            print ( 'zip_file_name: ', zip_file_name ) 

            # ziped_Model = fs.create_zip(UEfolder[0], zip_file_name)
            ziped_Model = fs.create_zip_Folder(UEfolder, zip_file_name)
            print ( 'ziped_Model: ', ziped_Model )
            # from smaug_cmd.adapter import fs
            # logger.info('Create "%s" Texture Zip: %s', text_key, ziped_texture)

            # 上傳至 OOS
            upload_zip_object_name = rfs.put_representation1( asset_id, zip_file_name, ziped_Model )

            # 把 ziped_texture 移至 .smaug 下
            moved_zip_file = fs.collect_to_smaug( asset_template["basedir"], ziped_Model )

            RepresentationOp.create(
                {
                    "assetId": asset_id,
                    "name": zip_file_name,

                    # check
                    "type": "MODEL",
                    "format": "IMG",
                    
                    "fileSize": os.path.getsize(moved_zip_file),
                    "uploaderId": upload_user,
                    "path": upload_zip_object_name,
                    "meta": {},
                }
            )
            logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)
        

                

        


        # keyword_group = ["_AvalonSource/texture", "_AvalonSource/texture_low"]
        # group_files = util.group_files_by_directory(asset_template["textures"])
        # filter_group_files = _filter_by_keywors(keyword_group, group_files)
        # texture_groups = {os.path.basename(k): v for k, v in filter_group_files.items()}
        # for text_key, files in texture_groups.items():
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
        #             "fileSize": os.path.getsize(moved_zip_file),
        #             "uploaderId": user_id,
        #             "path": upload_zip_object_name,
        #             "meta": {},
        #         }
        #     )
        #     logger.debug("Create DB record for Asset(%s): %s", asset_id, zip_file_name)
        



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
