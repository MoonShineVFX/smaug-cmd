import logging
from PySide6.QtCore import QObject
from smaug_cmd.domain.smaug_types import (

    AssetTemplate,
    AssetCreateResponse,
    AssetCreateParams,
    RepresentationCreateParams,
    RepresentationCreateResponse,
)

from smaug_cmd.model import data as ds

from smaug_cmd.domain.exceptions import SmaugOperaterError


logger = logging.getLogger("smaug_cmd.domain.op")


class AssetOp(QObject):
    @classmethod
    def create(cls, asset_template: AssetTemplate) -> AssetCreateResponse:
        if asset_template["categoryId"] is None:
            logger.error("Asset category id is None")
            raise SmaugOperaterError("Asset category id is None")
        param_payload: AssetCreateParams = {
            "name": asset_template["name"],
            "categoryId": asset_template["categoryId"],
            "tags": asset_template["tags"],
        }
        re = ds.create_asset(param_payload)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]


class RepresentationOp(QObject):
    @classmethod
    def create(
        cls, payload: RepresentationCreateParams
    ) -> RepresentationCreateResponse:
        re = ds.create_representation(payload)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        if re[1] is None:
            logger.error("Create representation return None")
            raise SmaugOperaterError("Create representation return None")
        else:
            return re[1]
