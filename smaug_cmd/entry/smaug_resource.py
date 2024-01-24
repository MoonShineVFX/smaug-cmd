import os
import logging
from typing import Generator
from smaug_cmd.bootstrap import bootstrap
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain import parsing as ps
from smaug_cmd.services.auth import log_in
from smaug_cmd.services.logic.resource_upload_logic import md_uploader
from smaug_cmd import setting

import json

logging.basicConfig(level=logging.INFO)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger("smaug_cmd.domain.resource_upload")

bootstrap(setting)


def smaug_resource_uploader(folder: str):
    """Upload a asset from resource team to smaug.

    :param base_dir: The base directory of the resource.
    :return: The resource id.
    """
    
    uploader_id = os.environ.get("UPLOADER_ID", "")
    uploader_pw = os.environ.get("UPLOADER_PW", "")

    log_in(uploader_id, uploader_pw)

    # 從所有的 md 檔組合出分類結構
    for md_file in _find_md_files(folder):
        # logger.info("PROCESSING: %s", os.path.basename(md_file))
        # md_file  "R:\_Asset\_Obsidian\MoonShineAsset\Unreal Asset\Unreal_AncientEast 古代東方場景.md"
        print ( 'md_file: ', md_file )
        md_json = ps.md_parsing(md_file)
        # from smaug_cmd.domain import parsing as ps

        
        #Yung Check
        # print ( 'md_json: ', md_json  )
        md_file_name = os.path.basename(md_file)[:-3]
        # from smaug_cmd.domain import parsing as ps
        md_json_path = 'E:/Repos/smaug-cmd/test_Yung/' + md_file_name + '.json'
        md_json_object = json.dumps(md_json, indent=4, ensure_ascii=False)
        with open( md_json_path, "w", encoding='UTF-8' ) as outfile:
            outfile.write(md_json_object)


        # print in json get more clean 
        # print ( json.dumps(md_json, indent=4, ensure_ascii=False) )
        # print ( 'md_json: ', md_json  )
            
        try:
            
            md_uploader(md_json)
            pass
            # print ( "md_json", md_json )
            # from smaug_cmd.services.logic.resource_upload_logic import md_uploader
        except SmaugError as e:
            logger.info(e)

        print ( 'upload Finish' )

def _find_md_files(md_file_folder) -> Generator[str, None, None]:
    for root, _, files in os.walk(md_file_folder):
        for file in files:
            if file.endswith(".md"):
                md_file = os.path.join(root, file).replace("\\", "/")
                yield md_file

                # print ( 'md_file: ', md_file )


if __name__ == "__main__":
    # UEAssetPath = 'R:/_Asset/_Obsidian/MoonShineAsset/Unreal Asset/'
    # UEAssetPath = 'C:/repos/smaugs/resource/_Asset/_Obsidian/MoonShineAsset/Unreal Asset/'
    AssetPath = 'C:/repos/smaugs/resource/_Asset/_Obsidian/MoonShineAsset/Taiwan/'
    smaug_resource_uploader(AssetPath)
    # smaug_resource_uploader(
    #     f"{os.environ.get('TEST_DATA_RESOURCE')}/_Obsidian/MoonShineAsset".replace("\\", "/")
    # )




    


