import logging
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
from smaug_cmd.domain.exceptions import SmaugApiError
from smaug_cmd.domain.smaug_types import UserInfo
from smaug_cmd import setting

logger = logging.getLogger("smaug_cmd.auth")


_session = Session()


def log_in(u: str, w: str) -> UserInfo:
    """登入"""
    login_api = f"{setting.api_root}/login"

    try:
        res = _session.post(login_api, auth=HTTPBasicAuth(u, w))
    except Exception as e:
        logger.error(str(e))
        raise SmaugApiError("登錄有誤") from e

    auth_token = _session.cookies.get("authToken")
    logger.debug(f"auth_token: {auth_token}")
    if auth_token:
        _session.headers.update({"Authorization": f"Bearer {auth_token}"})
    user_info:UserInfo = res.json()
    return (user_info)


def log_out():
    """登出"""
    logout_api = f"{setting.api_root}/logout"
    try:
        logout_resp = _session.post(logout_api)
    except Exception as e:
        print(e)
        return None
    return logout_resp.json()
