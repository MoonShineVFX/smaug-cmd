import logging
from typing import List, Optional
from PySide6.QtCore import QObject
from smaug_cmd.domain.smaug_types import (
    AssetTemplate,
    AssetCreateResponse,
    AssetCreateParams,
    CategoryCreateResponse,
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


class CategoryOp(QObject):
    @classmethod
    def create(
        cls, name: str, parent_id: Optional[int], menu_id: str
    ) -> CategoryCreateResponse:
        re = ds.create_category(name, parent_id, menu_id)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]

    @classmethod
    def getByName(cls, name: str) -> List[CategoryCreateResponse]:
        re = ds.get_categories_by_name(name)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]

    @classmethod
    def getByNameAndParent(cls, name: str, parent: Optional[str], menu_id:str) -> List[CategoryCreateResponse]:
        re = ds.get_categories_by_name_parent(name, parent, menu_id)
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]


class MenuOp(QObject):
    @classmethod
    def all(cls):
        re = ds.get_menus()
        # from smaug_cmd.model import data as ds
        if str(re[0])[0] != "2":
            logger.error(re[1]["message"])
            raise SmaugOperaterError(re[1]["message"])
        return re[1]


if __name__ == "__main__":
    # print(CategoryOp.getByName("Project 2019"))
    print( MenuOp.all() )
