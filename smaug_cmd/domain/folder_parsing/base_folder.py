import os
import logging
from typing import List, Optional
from smaug_cmd.adapter.smaug import SmaugJson
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.setting import (
    exclude_files,
    exclude_folders,
    texture_factors,
)
from smaug_cmd.domain.folder_parsing import util
from smaug_cmd.domain.folder_parsing.folder_typing import FolderType


logger = logging.getLogger("smaug_cmd.domain.folders")


def guess_preview_model(file_paths: List[str]) -> str | None:
    for file_path in file_paths:
        if file_path.split(".")[-1].lower() == "glb":
            return file_path
    return None


class BaseFolder:

    @classmethod
    def create_if_applicable(cls, folderpath:str)-> Optional["BaseFolder"]:
        """如果是可以建立的資料夾，就建立"""
        if cls.is_applicable(folderpath):
            return cls(folderpath)
        return None
    
    @classmethod
    def is_applicable(cls, folderpath:str)->bool:
        """判斷 folderpath 是否是此類別能處理的資料夾"""
        raise NotImplementedError

    def __init__(self, path: str, **kwargs):
        self._folder_type = FolderType.UNKNOWN
        self._path = path
        self._rawfilepaths: List[str] = []
        self._at: AssetTemplate = {
            "id": None,
            "name": "",
            "categoryId": None,
            "previews": [],  # 預覽圖
            "preview_model": "",  # 預覽模型
            "models": [],  # 模型
            "textures": [],  # 貼圖
            "renders": [],  # 渲染圖
            "meta": {},  # 其他資料(如果有)
            "tags": [],  # 標籤
            "basedir": self._path,  # 資料夾路徑
            "createAt": None,
            "updateAt": None,
        }
        self._init()
        self._init_from_smaug()

    def _init(self):
        # 取得資料夾的所有內容檔案
        for root, folders, files in os.walk(self._path):
            if os.path.basename(root) in exclude_folders:
                continue
            for file in files:
                if file in exclude_files:
                    continue
                self._rawfilepaths.append(os.path.join(root, file))
                file_path = os.path.join(root, file)
                if self.is_texture(file_path):
                    self._at["textures"].append(file_path)
                elif self.is_preview(file_path):
                    self._at["previews"].append(file_path)
                elif self.is_render_image(file_path):
                    self._at["renders"].append(file_path)
                elif self.is_model(file_path):
                    self._at["models"].append(file_path)
                else:
                    logger.debug("drop file : %s", file_path)

            for file in self._at["models"]:
                if self.is_3d_preview(file):
                    self._at["preview_model"] = file
                    self._at["models"].remove(file)
                    break

    def is_preview(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_render_image(self, file_path: str) -> bool:
        raise NotImplementedError

    def is_model(self, file_path: str) -> bool:
        if not util.validate_model_extension(file_path):
            return False
        return True

    def is_texture(self, file_path: str) -> bool:
        if not util.validate_tex_extension(file_path):
            return False

        if any([i in file_path.lower() for i in texture_factors]):
            return True
        return False

    def is_3d_preview(self, file_path: str) -> bool:
        """預設的 3d 預覽檔案判斷
        檔名以 "_preview.glb" 結束
        """
        if file_path.endswith("_preview.glb"):
            return True
        return False

    def _init_from_smaug(self):
        """從 smaug.json 資料夾中讀取資料"""
        if not os.path.exists(self._path + "/.smaug"):
            return
        sjosn = SmaugJson(self._path)
        data = sjosn.deserialize()
        self._at.update(data)

    def asset_template(self) -> AssetTemplate:
        return self._at

    def folder_type(self) -> FolderType:
        return self._folder_type