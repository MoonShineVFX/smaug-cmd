import logging
from typing import Optional
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.smaug_types import UserInfo
from smaug_cmd import setting

logger = logging.getLogger("smaug_cmd.auth")


_session = Session()
_user: Optional[UserInfo] = None


def log_in(u: str, w: str) -> UserInfo:
    """登入"""

    login_api = f"{setting.api_root}/login"
    print ( 'login_api: ', login_api )

    try:
        res = _session.post(login_api, auth=HTTPBasicAuth(u, w))
    except Exception as e:
        logger.error(str(e))
        raise SmaugApiError("登錄有誤") from e

    auth_token = _session.cookies.get("authToken")
    logger.debug(f"auth_token: {auth_token}")
    if auth_token:
        _session.headers.update({"Authorization": f"Bearer {auth_token}"})
    user_info: UserInfo = res.json()
    global _user
    _user = user_info
    return user_info


def log_out():
    """登出"""
    logout_api = f"{setting.api_root}/logout"
    try:
        logout_resp = _session.post(logout_api)
    except Exception as e:
        print(e)
        return None
    return logout_resp.json()


def current_user():
    """取得目前登入的使用者資訊"""
    return _user
