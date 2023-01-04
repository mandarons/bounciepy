from aioresponses import CallbackResult

from bounciepy.const import AUTH_TOKEN_URL, REST_API_BASE_URL
from tests import const


async def mock_response(url, **kwargs):
    url_str = str(url)
    print(kwargs)
    if AUTH_TOKEN_URL in url_str:
        return CallbackResult(
            status=200,
            payload=const.MOCK_AUTH_RESPONSE,
        )
    if REST_API_BASE_URL in url_str:
        if "/vehicles" in url_str:
            return CallbackResult(status=200, payload=const.MOCK_VEHICLES_RESPONSE)
        if "/user" in url_str:
            return CallbackResult(status=200, payload=const.MOCK_USER_RESPONSE)
        if "/trips" in url_str:
            return CallbackResult(status=200, payload=const.MOCK_TRIPS_RESPONSE_IMEI)
    return None
