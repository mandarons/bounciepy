from aioresponses import CallbackResult
from tests import const
from bounciepy.const import AUTH_TOKEN_URL, REST_API_BASE_URL, AUTH_GRANT_TYPE


async def mock_response(url, **kwargs):
    url_str = str(url)
    if AUTH_TOKEN_URL in url_str:
        if "data" in kwargs:
            data = kwargs["data"]
            if (
                "client_id" in data
                and data["client_id"] == const.MOCK_CLIENT_ID
                and "client_secret" in data
                and data["client_secret"] == const.MOCK_CLIENT_SECRET
                and "grant_type" in data
                and data["grant_type"] == AUTH_GRANT_TYPE
                and "code" in data
                and data["code"] == const.MOCK_AUTH_CODE
                and "redirect_uri" in data
                and data["redirect_uri"] == const.MOCK_REDIRECT_URI
            ):
                return CallbackResult(
                    status=200,
                    payload=const.MOCK_AUTH_RESPONSE,
                )
            else:
                # TODO return correct error
                pass
    if REST_API_BASE_URL in url_str:
        if "headers" in kwargs:
            headers = kwargs["headers"]
            if "Authorization" in headers:
                if const.MOCK_ACCESS_TOKEN == headers["Authorization"]:
                    if "/vehicles" in url_str:
                        return CallbackResult(
                            status=200, payload=const.MOCK_VEHICLES_RESPONSE
                        )
                    elif "/user" in url_str:
                        return CallbackResult(
                            status=200, payload=const.MOCK_USER_RESPONSE
                        )
                    elif "/trips" in url_str:
                        return CallbackResult(
                            status=200, payload=const.MOCK_TRIPS_RESPONSE_IMEI
                        )
                    else:
                        return CallbackResult(status=404)
                else:
                    return CallbackResult(status=401)
            else:
                return CallbackResult(
                    status=400, payload={"errors": "This was a bad request because..."}
                )
    return None
