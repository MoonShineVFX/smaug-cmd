import json
import time
from typing import List, Optional, Tuple, Dict, Any, Union

import logging
from urllib.parse import quote
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.smaug_types import (
    AssetCreateParams,
    AssetCreateResponse,
    CategoryDetailTree,
    CategoryCreateResponse,
    MenuTree,
    RepresentationCreateParams,
    RepresentationCreateResponse,
)
from smaug_cmd.services.auth import _session
from smaug_cmd import setting

logger = logging.getLogger("smaug_cmd.data")


class NestedDict:
    def __init__(self, value=None):
        self._data = {}
        self._value = value

    def __getitem__(self, key) -> "NestedDict":
        if key not in self._data:
            self._data[key] = NestedDict()
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __repr__(self):
        return repr(self._data)

    def value(self):
        return self._value


class CachedNestedDict:
    def __init__(self):
        self._data: Dict[Any, Union["CachedNestedDict", Any]] = {}
        self._timestamp: Dict[Any, float] = {}

    def _is_expired(self, key) -> bool:
        if key not in self._timestamp:
            return False
        elapsed_time = time.time() - self._timestamp[key]
        is_expired = elapsed_time > setting.cache_time
        if is_expired:  # 如果已過期，我們可以清除相關的數據
            del self._timestamp[key]
            del self._data[key]
        return is_expired

    def __setitem__(self, keys: Union[tuple, Any], value):
        current = self
        if not isinstance(keys, tuple):
            keys = (keys,)

        for key in keys[:-1]:
            if key not in current._data:
                current._data[key] = CachedNestedDict()
            current = current._data[key]

        current._data[keys[-1]] = NestedDict(value)
        current._timestamp[keys[-1]] = time.time()

    def __getitem__(
        self, keys: Union[tuple, Any]
    ) -> Union[NestedDict, "CachedNestedDict"]:
        current = self
        if not isinstance(keys, tuple):
            keys = (keys,)

        for idx, key in enumerate(keys):
            if isinstance(current, CachedNestedDict) and current._is_expired(key):
                return NestedDict()  # 返回一個空的 NestedDict

            if key not in current._data:
                # 如果是最後一個鍵，則添加一個NestedDict；否則，添加一個CachedNestedDict
                current._data[key] = (
                    NestedDict() if idx == len(keys) - 1 else CachedNestedDict()
                )

            current = current._data[key]

        return current  # 在此返回當前的對象，它應該是一個NestedDict

    def __repr__(self):
        return repr(self._data)


__data = CachedNestedDict()


def get_menus():
    """取得所有的 categories"""
    minus_api = f"{setting.api_root}/menus"
    cached_value = __data[("menus",)].value()
    if cached_value:
        return cached_value
    try:
        res = _session.get(minus_api)
    except Exception as e:
        logger.warning(e)
        return None
    menus_data = res.json()
    logger.debug(f"menus_data: {menus_data}")
    __data[("menus",)] = (res.status_code, menus_data)
    return __data[("menus",)].value()


def get_menu_tree(menu_id) -> Tuple[int, MenuTree | Dict[str, str]]:
    """取得所有的 categories"""
    api = f"{setting.api_root}/menuTree"
    menu_tree_api = f"{api}?id={menu_id}"
    cache_key = (api, "id", menu_id)
    cache_value = __data[cache_key].value()

    if cache_value:
        return cache_value

    try:
        res = _session.get(menu_tree_api)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    menu_tree_data = res.json()
    the_value = (res.status_code, menu_tree_data)
    __data[cache_key] = the_value
    return the_value


def get_category(category_id, force=False) -> Tuple[int, CategoryDetailTree]:
    api = f"{setting.api_root}/trpc/category.tree"
    params = {0: {"json": {"categoryId": category_id}}}
    params_str = json.dumps(params)
    encode_params = quote(params_str)
    category_tree = f"{api}?batch=1&input={encode_params}"
    cache_key = (api, "categoryId", category_id)
    # cache_value = __data[cache_key].value()

    if not force:
        cache_value = __data[cache_key].value()
        if cache_value:
            return cache_value

    try:
        res = _session.get(category_tree)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    category_data = res.json()[0]
    return_value = (res.status_code, category_data["result"]["data"]["json"]["detail"])
    __data[cache_key] = return_value
    return return_value


def create_asset(
    payload: AssetCreateParams,
) -> Tuple[int, AssetCreateResponse | Dict[str, str]]:
    api = f"{setting.api_root}/trpc/assets.create"
    api_payload = {"0": {"json": payload}}
    asset_create_api = f"{api}?batch=1"
    try:
        res = _session.post(asset_create_api, json=api_payload)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    asset_data = res.json()[0]
    the_value = (res.status_code, asset_data["result"]["data"]["json"]["detail"])
    return the_value


def create_representation(
    payload: RepresentationCreateParams,
) -> Tuple[int, RepresentationCreateResponse | Dict[str, str]]:
    api = f"{setting.api_root}/trpc/representation.create"
    api_payload = {"0": {"json": payload}}
    representation_create_api = f"{api}?batch=1"
    try:
        res = _session.post(representation_create_api, json=api_payload)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    representation_data = res.json()[0]
    the_value = (
        res.status_code,
        representation_data["result"]["data"]["json"]["detail"],
    )
    return the_value


def create_category(
    name: str, parent_id: Optional[int], menu_id: str
) -> Tuple[int, CategoryCreateResponse | Dict[str, str]]:
    api = f"{setting.api_root}/trpc/categories.create"
    api_payload = (
        {"0": {"json": {"name": name, "parentId": parent_id, "menuId": menu_id}}}
        if parent_id
        else {"0": {"json": {"name": name, "menuId": menu_id}}}
    )
    category_create_api = f"{api}?batch=1"
    try:
        res = _session.post(category_create_api, json=api_payload)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    category_data = res.json()[0]
    if "error" in category_data:
        raise SmaugApiError(category_data["error"]["json"]["message"])
    the_value = (res.status_code, category_data["result"]["data"]["json"]["detail"])
    return the_value


def get_categories_by_name(
    name: str,
) -> Tuple[int, Dict[str, str] | List[CategoryCreateResponse]]:
    api = f"{setting.api_root}/trpc/categories.getByName"
    api_payload = {"0": {"json": {"name": name}}}
    api_payload_str = json.dumps(api_payload)
    encode_params = quote(api_payload_str)
    full_api = f"{api}?batch=1&input={encode_params}"
    try:
        res = _session.get(full_api)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    categories_data = res.json()[0]
    the_value = (res.status_code, categories_data["result"]["data"]["json"]["list"])
    return the_value


def get_categories_by_name_parent(name: str, parnet_name: Optional[str], menu_id: str) -> Tuple[int, Dict[str, str] | List[CategoryCreateResponse]]:
    
    api = f"{setting.api_root}/trpc/categories.getByNameAndParent"
    api_payload = {"0": {"json": {"name": name, "parent": parnet_name, "menuId": menu_id}}}
    api_payload_str = json.dumps(api_payload)
    encode_params = quote(api_payload_str)
    full_api = f"{api}?batch=1&input={encode_params}"
    try:
        res = _session.get(full_api)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    categories_data = res.json()[0]
    the_value = (res.status_code, categories_data["result"]["data"]["json"]["list"])
    return the_value


# if __name__ == "__main__":
# login_in("admin", "admin")
# cates = get_categories_by_name("Project 2019")
# print(cates[1][0]["id"])
