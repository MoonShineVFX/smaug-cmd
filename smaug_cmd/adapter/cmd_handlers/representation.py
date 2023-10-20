from smaug_cmd.domain import command as cmd
from smaug_cmd.services import remote_fs as rfs
from smaug_cmd.model import data as ds


def upload_representation(data: cmd.UploadRepresentation) -> str:

    # 產生 zip 檔名
    re = rfs.put_representation1(data.asset_id, data.file_path, data.object_name)
    if str(re[0])[0] != '2':
        raise Exception(re[1]["message"])
    return re[1]


def create_representation(data: cmd.CreateRepresentation) -> str:
    ds.create_representation(**data.dict())