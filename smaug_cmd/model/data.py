
from typing import Optional
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
import logging
import smaug_cmd.setting as setting
from smaug_cmd.domain.smaug_types import MenuTree


logger = logging.getLogger('data')
logger.setLevel(logging.DEBUG)


_session = Session()


__data = []


def login_in(u: str, w: str) -> Optional[dict]:
    ''' 登入 '''
    login_api = f'{setting.api_root}/login'
 
    try:
        login_resp = _session.post(login_api, auth=HTTPBasicAuth(u, w))
    except Exception as e:
        logger.warning(e)
        return None
    auth_token = _session.cookies.get("authToken")
    logger.debug(f"auth_token: {auth_token}")
    if auth_token:
        _session.headers.update({"Authorization": f"Bearer {auth_token}"})

    return login_resp.json()


def get_menus():
    ''' 取得所有的 categories '''
    categories_api = f'{setting.api_root}/menus'
    try:
        categories_resp = _session.get(categories_api)
    except Exception as e:
        logger.warning(e)
        return None
    categories_data = categories_resp.json()
    return categories_data


def get_menu_tree(menu_id) -> MenuTree:
    ''' 取得所有的 categories '''
    categories_api = f'{setting.api_root}/categories?={menu_id}'
    try:
        categories_resp = _session.get(categories_api)
    except Exception as e:
        print(e)
        return None
    categories_data = categories_resp.json()
    return categories_data


def log_out():
    ''' 登出 '''
    logout_api = f'{setting.api_root}/logout'
    try:
        logout_resp = _session.post(logout_api)
    except Exception as e:
        print(e)
        return None
    return logout_resp.json()


if __name__=='__main__':
    login_in('admin', 'admin')
    menus = get_menus()
    for menu in menus:
        print(get_menu_tree(menu['id']))