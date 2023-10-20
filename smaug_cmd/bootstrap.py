import logging

import smaug_cmd.services.remote_fs as rfs

logger = logging.getLogger("smaug-cmd.bootstrap")


def bootstrap(setting):
    logger.info("bootstrap")
    rfs.init(setting.minio_endpoint, setting.minio_access_key, setting.minio_secret_key)
    logger.info("bootstrap-Done")
