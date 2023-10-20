import logging
import os
from typing import Any, Callable, Dict, List, Optional
from minio import Minio
from minio.error import S3Error
from functools import partial

logger = logging.getLogger("smaug-cmd.adapter")


client = Minio(
    os.environ["MINIO_HOST"],
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False,
)


def _makesure_bucket_exist(bucket_name):
    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
    except S3Error as e:
        logger.error(e)
        raise RuntimeError("smaug folder has error") from e


makesure_smaug_bucket_exist = partial(_makesure_bucket_exist, "smaug")


def put_file(file_path, object_name) -> str:
    makesure_smaug_bucket_exist()
    result = client.fput_object(
        "smaug",
        object_name,
        file_path,
    )
    logger.debug("'%s' is successfully uploaded as object '%s'" % (file_path, result.object_name))
    return result.object_name


def put_representation(asset_id: str, asset_name: str, file_path: str):
    """Upload representation file to smaug."""
    file_name = os.path.basename(file_path).split(".")[0]
    file_extension = os.path.splitext(file_path)[-1].lower()
    object_name = f"/{asset_id}/{asset_name}_{file_name}{file_extension}"
    uploaded_object_name = put_file(file_path, object_name)
    logger.debug(f"representation file {uploaded_object_name} is uploaded")
    return uploaded_object_name


def put_preview(asset_id, asset_name, preview_file) -> str:
    """Upload preview file to smaug."""
    def object_name_format(idx, file_path, type):
        file_extension = os.path.splitext(file_path)[-1].lower()
        object_name = f"/{asset_id}/{asset_name}_{type}-{idx}{file_extension}"
        return object_name

    return put_representation(asset_id, asset_name, object_name_format(1, preview_file, "preview"))

def put_previews(asset_id, asset_name, preview_files) -> List[str]:
    """Upload preview files to smaug."""



    return [
        
        for idx, file_path in enumerate(preview_files)
    ]


def put_textures(asset_id, asset_name, texture_zips):
    """Upload texture zip files to smaug."""

    return [_upload(file, t_key) for t_key, file in texture_zips.items()]


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
