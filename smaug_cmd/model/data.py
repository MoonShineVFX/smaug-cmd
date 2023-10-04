from typing import Optional, Tuple, Dict
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
import logging
import smaug_cmd.setting as setting
from smaug_cmd.domain.smaug_types import MenuTree


logger = logging.getLogger("smaug-cmd.data")


_session = Session()


__data = []


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
    try:
        res = _session.get(minus_api)
    except Exception as e:
        logger.warning(e)
        return None
    menus_data = res.json()
    logger.debug(f"menus_data: {menus_data}")
    return (res.status_code, menus_data)


def get_menu_tree(menu_id) -> Tuple[int, MenuTree | Dict[str, str]]:
    """取得所有的 categories"""
    menu_tree_api = f"{setting.api_root}/menuTree?id={menu_id}"
    try:
        res = _session.get(menu_tree_api)
    except Exception as e:
        logger.warning(e)
        return (500, {"message": str(e)})
    menu_tree_data = res.json()
    return (res.status_code, menu_tree_data)


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
    login_in("admin", "admin")
    menus = get_menus()
    for menu in menus:
        print(get_menu_tree(menu["id"]))
