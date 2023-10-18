import logging
import os
from minio import Minio
from minio.error import S3Error
from functools import partial

logger = logging.getLogger("smaug-cmd.adapter")


client = Minio(
    os.environ["MINIO_HOST"],
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    secure=False
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


def upload_file(file_path, object_name)-> str:    
    makesure_smaug_bucket_exist()
    result = client.fput_object("smaug", object_name, file_path,)
    logger.debug( "'%s' is successfully uploaded as object '%s'" % (file_path, result.object_name))
    return result.object_name


def upload_previews(asset_id, preview_files):
    """Upload preview files to smaug."""
    for preview_file in preview_files:
        # upload preview file to smaug
        file_name = os.path.basename(preview_file)
        file_extension = os.path.splitext(preview_file)[-1].lower()
        object_name = f"/{asset_id}/{file_name}_preview{file_extension}"
        uploaded_object_name = upload_file(preview_file, object_name)
        logger.debug(f"preview file {uploaded_object_name} is uploaded")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)