import os
from pathlib import PureWindowsPath
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.upload_strategies import UnrealResourceUploader


class UnrealResourceFolder(BaseFolder):
    # ava_folder = "_AvalonSource"
    ue_folder = "Game_Unreal"

    def __init__(self, path: str, upload_strategies: UnrealResourceUploader):
        super().__init__(path, upload_strategies)
        self.set_folder_type(FolderType.UASSET_MODEL)

        print ( 'self.set_folder_type:', self.set_folder_type )

    @classmethod
    def is_applicable(cls, folderpath: str) -> bool:
        # return is_avalon_source_model_folder(folderpath)
        return is_Unreal_source_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        # 確認是否是圖檔
        if not util.validate_tex_extension(file_path):
            return False

        # 確是上面不是 C D 之類的根目錄
        asset_pathobj = PureWindowsPath(file_path)
        if not asset_pathobj.parent.name:
            return False

        return True

    def is_render_image(self, file_path: str) -> bool:
        """目前沒有渲染圖"""
        return False

    def is_model(self, file_path: str) -> bool:
        # UE 不用打包3D檔案 只需要素材包路徑 如果沒有路徑就報錯 需手動進入資料夾解壓或是重新下載素材
        # Yung add
        # print ( '>>>> file_path: ', file_path )

        # if not util.validate_model_extension(file_path):
        #     return False

        # for path_part in PureWindowsPath(file_path).parts:
        #     if self.ava_folder.lower() in path_part.lower():
        #         return True
        return False

    def is_texture(self, file_path: str) -> bool:
        # unreal 素材包沒有材質 整包打包
        # if not util.validate_tex_extension(file_path):
        #     return False
        # if file_path.find(self.ava_folder + "/texture"):
        #     return True
        return False

def is_Unreal_source_model_folder(folder_path: str):
    # """判是否為 ResourceFolderType.AVALON_SOURCE_MODEL 資料夾"""
    
    # yung add 
    print ( 'folder_path: ', folder_path )
    folders = folder_path
    folder_required = "Game_Unreal"

    if folder_required in folders:
        return True
    # for folder in util.list_dir(folder_path):
    #     # print ( 'folder: ', folder )
    #     if folder_required in folder:
    #     # if not os.path.isfile(folder):
    #         print ( 'folder: ', folder )
    #     # if folder.lower() == folder_required:
    #     #     return True
    # return False


# def is_avalon_source_model_folder(folder_path: str):
#     """判是否為 ResourceFolderType.AVALON_SOURCE_MODEL 資料夾"""

#     # 要有 _AvalonSource
#     folder_required = "_avalonsource"
#     for folder in util.list_dir(folder_path):
#         if folder.lower() == folder_required:
#             return True
#     return False


if __name__=='__main__':
    folder = "R:/_Asset/Game_Unreal/AncientEast/AsianTemple/"
    # UnrealResourceFolder( folder, UnrealResourceUploader )
    
    print( UnrealResourceFolder.is_applicable(folder) )
