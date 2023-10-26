import logging
from typing import Dict, List, Optional, Tuple, Callable
import os
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox, QLabel, QPushButton

from smaug_cmd.adapter.cmd_handlers import handler
from smaug_cmd.domain.smaug_types import (
    Menu,
    MenuTree,
    AssetFolderType,
    AssetTemplate
)
from smaug_cmd.model import login_in as api_login
from smaug_cmd.model import data as ds
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain import command as cmd


logger = logging.getLogger("smaug-cmd.domain")


class SmaugCmdHandler(QObject):
    def __init__(self):
        super().__init__(None)
        self.current_user = None

    def error_handler(self, error_msg, er_cb: Optional[Callable] = None):
        logger.error(error_msg)
        er_cb if er_cb(error_msg) else None

    def log_in(self, user_name, password) -> Optional[Tuple[int, dict]]:
        re = api_login(user_name, password)
        if re is None:
            self.error_handler("Login error, server not response.", lambda x: QMessageBox.critical(None, "Error", x))
            return re
        if str(re[0])[0] == "2":
            self.current_user = re[1]
            return re
        else:
            self.error_handler(re[1]["message"], )
            return re

    def get_menus(self, error_cb: Optional[Callable]) -> Optional[List[Menu]]:
        re = ds.get_menus()
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def get_menu_tree(
        self, menu_id, error_cb: Optional[Callable] = None
    ) -> Optional[MenuTree]:
        re = ds.get_menu_tree(menu_id)
        if str(re[0])[0] != "2":
            self.error_handler(re[1]["message"], error_cb)
            return None
        return re[1]

    def _setup_cate_breadcrumb(
        self, cate: int, cate_lbl: QLabel, cate_picker_btn: QPushButton
    ):
        """Compose the category breadcrumb."""
        # 取的分類的父分類
        cate_query = ds.get_category(cate)
        if str(cate_query[0])[0] != 2:
            self.error_handler(cate_query[1]["message"])
            return
        cate_detail = cate_query[1]

        # 設定 UI
        cate_lbl.setText(f"category: {cate_detail['breadCrumb']}")
        cate_picker_btn.setProperty("smaug_cate", True)
        return

    def asset_template(self, folder_path) -> Optional[AssetTemplate]:
        # convert folder to asset template
        if ps.is_asset_model_folder(folder_path) == AssetFolderType.UNKNOWN:
            return None
        return ps.folder_asset_template(folder_path)

    def create_asset_proc(self, asset_template: AssetTemplate, ui_cb: Callable = None):
        """在資料庫建立 asset 的流程
        建立 asset 以取得 asset id 後
        會處理模型檔跟貼圖檔的分類之後壓縮成 zip 檔案
        各別上傳完 zip 檔之後再去資料庫建立 representation
        """

        create_payload = cmd.CreateAsset(
            asset_template["category_id"],
            asset_template["name"],
            asset_template["tags"],
        )
        # 建立 asset 以取得 asset id
        asset_id = handler(create_payload)["id"]
        asset_name = asset_template["name"]

        logger.debug("Asset(%s) Created", asset_id)
        if ui_cb:
            ui_cb(f"Asset({asset_id}) Created")

        smaug_commands = list()
        # upload preview command
        for idx, preview_file in enumerate(asset_template["previews"]):
            file_extension = os.path.splitext(preview_file)[-1].lower()
            object_name = f"{asset_name}_preview-{idx}{file_extension}"
            smaug_commands.append(
                (
                    cmd.UploadRepresentation(asset_id, preview_file, object_name),
                    f"Upload {preview_file} as {object_name}",
                )
            )
            smaug_commands.append(
                (
                    cmd.CreateRepresentation(
                        asset_id,
                        object_name,
                        "PREVIEW",
                        "IMG",
                        os.path.getsize(preview_file),
                        self.current_user["id"],
                    ),
                    f"Create Preview Representation \"{object_name}\"",
                )
            )

        # upload render command
        for idx, render_file in enumerate(asset_template["renders"]):
            file_extension = os.path.splitext(preview_file)[-1].lower()
            new_name = f"{asset_name}_render-{idx}{file_extension}"
            smaug_commands.append(
                (
                    cmd.UploadRepresentation(asset_id, render_file, new_name),
                    f"Upload {render_file} as {new_name}",
                )
            )
            smaug_commands.append(
                (
                    cmd.CreateRepresentation(
                        asset_id,
                        new_name,
                        "RENDER",
                        "IMG",
                        os.path.getsize(render_file),
                        self.current_user["id"],
                    ),
                    f"Create Render Representation {new_name}"
                    
                )
            )



        zip_process_cmds = list()
        # splite textures to texture-group,
        texture_groups = ps.texture_group(asset_id, asset_template["textures"])
        for text_key, files in texture_groups.items():
            # make texture zip payload
            zip_file_name = object_name = f"{asset_name}_{text_key}_textures.zip"
            zip_process_cmds.append(
                (cmd.CreateZip(files, zip_file_name), f"Create \"{text_key}\" Texture Zip")
            )

        # splite models to model-group
        model_groups = ps.model_group(asset_id, asset_template["models"])
        for model_key, files in model_groups.items():
            # make model zip payload
            zip_file_name = object_name = f"{asset_name}_{model_key}_models.zip"
            zip_process_cmds.append(
                (cmd.CreateZip(files, zip_file_name), f"Create \"{model_key}\" Model Zip")
            )


        #---------------------    
        # upload preview model process
        # upload textures process
        # upload models process
        # upload renders process
        # update meta data, find bounding box, find texture size, find model size..., etc.
        # update tags



