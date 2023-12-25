import logging
import os
from smaug_cmd.adapter import fs
from smaug_cmd.domain.smaug_types import AssetTemplate
from smaug_cmd.domain.upload_strategies.upload_strategy import UploadStrategy
from smaug_cmd.services import remote_fs as rfs

logger = logging.getLogger("smaug_cmd.domain.upload_strategy")


class AvalonResourceUploader(UploadStrategy):

    def upload_textures(self, asset_template: AssetTemplate, user_id: str):
        raise NotImplementedError
