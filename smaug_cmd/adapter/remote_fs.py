import logging
import os
from minio import Minio
from minio.error import S3Error
from functools import partial

logger = logging.getLogger("smaug-cmd.adapter")


client = Minio(
    os.environ["MINIO_URL"],
    access_key=os.environ["MINIO_ROOT_USER"],
    secret_key=os.environ["MINIO_ROOT_PASSWORD"],
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


def upload_file(respresentation, file_path):
    pass




    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "asiatrip", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
    )
    print(
        "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
        "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)