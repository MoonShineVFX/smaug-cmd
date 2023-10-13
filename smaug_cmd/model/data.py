import json
import time
from typing import Optional, Tuple, Dict, Any, Union
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
import logging
from urllib.parse import quote
from smaug_cmd.domain.smaug_types import MenuTree, CategoryDetailTree
from smaug_cmd import setting

logger = logging.getLogger("smaug-cmd.data")


_session = Session()

class NestedDict:
    def __init__(self, value=None):
        self._data = {}
        self._value = value

    def __getitem__(self, key) -> 'NestedDict':
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
        self._data: Dict[Any, Union['CachedNestedDict', Any]] = {}
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

    def __getitem__(self, keys: Union[tuple, Any]) -> Union[NestedDict, 'CachedNestedDict']:
        current = self
        if not isinstance(keys, tuple):
            keys = (keys,)

        for idx, key in enumerate(keys):
            if isinstance(current, CachedNestedDict) and current._is_expired(key):
                return NestedDict()  # 返回一個空的 NestedDict

            if key not in current._data:
                # 如果是最後一個鍵，則添加一個NestedDict；否則，添加一個CachedNestedDict
                current._data[key] = NestedDict() if idx == len(keys) - 1 else CachedNestedDict()
                
            current = current._data[key]

        return current  # 在此返回當前的對象，它應該是一個NestedDict

    def __repr__(self):
        return repr(self._data)


__data = CachedNestedDict()


def login_in(u: str, w: str) -> Optional[dict]:
    """登入"""
    login_api = f"{setting.api_root}/login"

    try:
        res = _session.post(login_api, auth=HTTPBasicAuth(u, w))
    except Exception as e:
        logger.warning(e)
        return None
    auth_token = _session.cookies.get("authToken")
    logger.debug(f"auth_token: {auth_token}")
    if auth_token:
        _session.headers.update({"Authorization": f"Bearer {auth_token}"})

    return (res.status_code, res.json())


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


def get_category(category_id) -> Tuple[int, CategoryDetailTree]:
    api = f"{setting.api_root}/trpc/category.tree"
    params = {0:{"json":{"categoryId":category_id}}}
    params_str = json.dumps(params)
    encode_params = quote(params_str)
    category_tree= f"{api}?batch=1&input={encode_params}"
    cache_key = (api, "categoryId", category_id)
    cache_value = __data[cache_key].value()
    if cache_value:
        return cache_value
    try:
        res = _session.get(category_tree)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    category_data = res.json()[0]
    the_value = (res.status_code, category_data['result']['data']['json']['detail'])
    return_value = (res.status_code, the_value)
    __data[cache_key] = return_value
    return return_value


def log_out():
    """登出"""
    logout_api = f"{setting.api_root}/logout"
    try:
        logout_resp = _session.post(logout_api)
    except Exception as e:
        print(e)
        return None
    return logout_resp.json()


if __name__ == "__main__":
    # login_in("admin", "admin")
    menus = get_menus()
    for menu in menus:
        print(get_menu_tree(menu["id"]))
