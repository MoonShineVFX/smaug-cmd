from smaug_cmd.domain import command as cmd
from smaug_cmd.services import remote_fs as rfs
from smaug_cmd.model import data as ds
from smaug_cmd.domain.exceptions import SmaugApiError


def upload_representation(payload: cmd.UploadFile) -> str:

    # 產生 zip 檔名
    try:
        re = rfs.put_representation1(payload.asset_id, payload.file_path, payload.object_name)
    except Exception as e:
        raise SmaugApiError() from e
    if str(re[0])[0] != '2':
        raise Exception(re[1]["message"])
    return re[1]


def create_representation(payload: cmd.CreateRepresentation) -> str:
    ds.create_representation(**payload.dict())
    