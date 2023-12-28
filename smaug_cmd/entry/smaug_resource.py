import os
import logging
from typing import Generator
from smaug_cmd.bootstrap import bootstrap
from smaug_cmd.domain.exceptions import SmaugError
from smaug_cmd.domain import parsing as ps
from smaug_cmd.services.logic.resource_upload_logic import md_uploader
from smaug_cmd import setting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smaug_cmd.domain.resource_upload")

bootstrap(setting)


def smaug_resource_uploader(folder: str):
    """Upload a asset from resource team to smaug.

    :param base_dir: The base directory of the resource.
    :return: The resource id.
    """

    # 從所有的 md 檔組合出分類結構
    for mb_file in _find_md_files(folder):
        md_json = ps.md_parsing(mb_file)
        try:
            md_uploader(md_json)
        except SmaugError as e:
            logger.info(e)


def _find_md_files(md_file_folder) -> Generator[str, None, None]:
    for root, _, files in os.walk(md_file_folder):
        for file in files:
            if file.endswith(".md"):
                md_file = os.path.join(root, file).replace("\\", "/")
                yield md_file


if __name__ == "__main__":
    smaug_resource_uploader(
        f"{os.environ.get('TEST_DATA_RESOURCE')}/_Obsidian/MoonShineAsset".replace("\\", "/")
    )
