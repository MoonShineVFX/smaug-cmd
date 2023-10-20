from dataclasses import asdict
from smaug_cmd.domain.smaug_types import AssetCreateResponse
from smaug_cmd.domain import command as cmd
from smaug_cmd.model import data as ds


def create_asset(payload: cmd.CreateAsset) -> AssetCreateResponse:
    """將 textures 壓成 zip 檔案"""
    # 產生 zip 檔名
    re = ds.create_asset(**asdict(payload))
    if str(re[0])[0] != '2':
        raise Exception(re[1]["message"])
    return re[1]

