import os
from typing import Generator
from smaug_cmd.domain import parsing as ps
from smaug_cmd.domain.upload_strategies.resource_uploader import md_uploader


def smaug_resource_uploader(folder: str):
    """Upload a asset from resource team to smaug.

    :param base_dir: The base directory of the resource.
    :return: The resource id.
    """

    # 從所有的 md 檔組合出分類結構
    for mb_file in _find_md_files(folder):
        md_json = ps.md_parsing(mb_file)
        md_uploader(md_json)


def _find_md_files(md_file_folder) -> Generator[str, None, None]:
    for root, _, files in os.walk(md_file_folder):
        for file in files:
            if file.endswith(".md"):
                md_file = os.path.join(root, file)
                yield md_file


if __name__ == "__main__":
    smaug_resource_uploader(
        f"{os.environ.get('TEST_DATA_RESOURCE')}\\_Obsidian\\MoonShineAsset"
    )
