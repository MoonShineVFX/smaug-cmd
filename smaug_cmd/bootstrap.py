import logging

import smaug_cmd.services.remote_fs as rfs

logger = logging.getLogger("smaug_cmd.bootstrap")


def bootstrap(setting):
    logger.info("bootstrap")
    rfs.init(setting.minio_host, setting.minio_root_user, setting.minio_root_password)
    logger.info("bootstrap-Done")
