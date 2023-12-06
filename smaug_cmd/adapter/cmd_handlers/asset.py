# from dataclasses import asdict
from dataclasses import asdict
import logging
from typing import cast
from smaug_cmd.domain.smaug_types import AssetCreateResponse
from smaug_cmd.domain import command as cmd
from smaug_cmd.model import data as ds
from smaug_cmd.domain.smaug_types import MenuTree

logger = logging.getLogger("smaug-cmd.adapter.cmd_handlers.asset")


def create_asset(payload: cmd.CreateAsset) -> AssetCreateResponse:
    """在資料庫中建立 asset"""

    logger.debug("Create Asset: %s", payload)
    create_param = asdict(payload)
    result = ds.create_asset(create_param)
    if str(result[0])[0] != "2":
        logger.error(result[1]["message"])
        raise RuntimeError("Can't create asset")
    return cast(AssetCreateResponse, result[1])


def asset_categories() -> MenuTree:
    """取得資料庫中的 asset 分類列表(Home)"""
    logger.debug("List Asset")
    result1 = ds.get_menus()
    if str(result1[0])[0] != "2":
        logger.error(result1[1]["message"])
        raise RuntimeError("Can't find menus")
    
    menu_id = next(iter([menu['id'] for menu in result1[1] if menu['name']=="Home"]), None)
    if menu_id is None:
        raise RuntimeError("Can't find menu id")

    result2 = ds.get_menu_tree(menu_id)
    if str(result2[0])[0] != "2":
        logger.error(result2[1]["message"])
        raise RuntimeError("Can't find categories by menu id")
    menutree = cast(MenuTree, result2[1])
    return menutree