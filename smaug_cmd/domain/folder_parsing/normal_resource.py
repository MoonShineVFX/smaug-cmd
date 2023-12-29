import os
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.taiwan_culture import is_taiwan_culture_model_folder
from smaug_cmd.domain.folder_parsing.asset_depart import is_asset_depart_model_folder
from smaug_cmd.domain.folder_parsing.base_folder import BaseFolder
from smaug_cmd.domain.upload_strategies.normal_resource import NormalResourceUploadStrategy


class NormalResourceModelFolder(BaseFolder):
    def __init__(self, path: str, upload_strategy:NormalResourceUploadStrategy):
        super().__init__(path, upload_strategy)
    
    @classmethod
    def is_applicable(cls, folderpath:str)->bool:
        return is_normal_resource_model_folder(folderpath)

    def is_preview(self, file_path: str) -> bool:
        # 確認是否是圖檔
        if not util.validate_tex_extension(file_path):
            return False
        
        # 是否在目録第一層
        folder = os.path.dirname(file_path)
        if folder.lower() != self._at["basedir"].lower():
            return False
        return True

    def is_render_image(self, file_path: str) -> bool:
        """目前沒有渲染圖"""
        return False

    def is_model(self, file_path: str) -> bool:
        if not util.validate_model_extension(file_path):
            return False
        return True

    def is_texture(self, file_path: str) -> bool:
        # 確認是否是圖檔
        if not util.validate_tex_extension(file_path):
            return False
        
        text_folder = ['texture', 'tex', 'texture_jpg']
        folder = os.path.basename(os.path.dirname(file_path))
        if folder.lower() not in text_folder:
            return False
        return True


def is_normal_resource_model_folder(folder_path: str):
    """判斷是否為 ResourceFolderType.NORMAL_RESOURCE_MODEL
    這個規格跟 taiwan_culture, asset_depart 有重疊，先確認是否為上述資料夾，如果是就不用再判斷是否為 normal 資料夾
    """
    
    if is_taiwan_culture_model_folder(folder_path):
        return False
    if is_asset_depart_model_folder(folder_path):
        return False

    texture_folder_variant = ["Texture", "tex"]
    items = util.list_dir(folder_path)
    items = [i.lower() for i in items]
    if not any([i.lower() in items for i in texture_folder_variant]):
        return False
    return True