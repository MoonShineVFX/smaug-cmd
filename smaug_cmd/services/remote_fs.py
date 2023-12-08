import logging
import os
# from typing import Any, Callable, Dict, List, Optional
from minio import Minio
from minio.error import S3Error
from functools import partial
from smaug_cmd.domain.exceptions import SmaugApiError

logger = logging.getLogger("smaug-cmd.adapter")


client = None

def init(endpoint, access_key, secret_key):
    global client
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,)


def check_client(func):
    def wrapper(*args, **kwargs):
        global client
        if client is None:
            raise RuntimeError("remote_fs is not initialized")
        return func(*args, **kwargs)
    return wrapper


def _makesure_bucket_exist(bucket_name):
    global client
    if client is None:
        raise RuntimeError("remote_fs is not initialized")
    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
    except S3Error as e:
        logger.error(e)
        raise RuntimeError("smaug folder has error") from e


makesure_smaug_bucket_exist = partial(_makesure_bucket_exist, "smaug")


@check_client
def put_file(file_path, object_name) -> str:
    makesure_smaug_bucket_exist()
    global client
    result = client.fput_object(
        "smaug",
        object_name,
        file_path,
    )
    logger.debug("'%s' is successfully uploaded as object '%s'" % (file_path, result.object_name))
    return result.object_name


@check_client
def put_representation(asset_id: str, file_path: str, object_name: str=None):
    file_name = os.path.basename(file_path)
    if not object_name:
        object_name = f"/{asset_id}/{file_name}"
    uploaded_object_name = put_file(file_path, object_name)
    logger.debug(f"representation file {uploaded_object_name} is uploaded")
    return uploaded_object_name


@check_client
def put_representation1(asset_id: str, asset_name: str, file_path: str):
    """Upload representation file to smaug."""
    file_name = os.path.basename(file_path).split(".")[0]
    file_extension = os.path.splitext(file_path)[-1].lower()
    object_name = f"/{asset_id}/{asset_name}_{file_name}{file_extension}"
    try:
        uploaded_object_name = put_file(file_path, object_name)
    except Exception as e:
        logger.error(e)
        raise SmaugApiError(f"Upload File Error:{file_name}") from e
    logger.debug(f"representation file {uploaded_object_name} is uploaded")
    return uploaded_object_name


@check_client
def put_preview(asset_id, asset_name, preview_file) -> str:
    """Upload preview file to smaug."""
    def object_name_format(idx, file_path, type):
        file_extension = os.path.splitext(file_path)[-1].lower()
        object_name = f"/{asset_id}/{asset_name}_{type}-{idx}{file_extension}"
        return object_name

    return put_representation1(asset_id, asset_name, object_name_format(1, preview_file, "preview"))

