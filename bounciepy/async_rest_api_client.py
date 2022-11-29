from aiohttp import ClientSession, ClientTimeout
from typing import Optional
from bounciepy.exceptions import (
    BadRequestError,
    InternalError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from bounciepy.const import (
    REST_API_BASE_URL,
    AUTH_TOKEN_URL,
    AUTH_GRANT_TYPE,
    API_DEFAULT_TIMEOUT_SECONDS,
)


class AsyncRESTAPIClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        auth_code: str,
        state: Optional[str] = "init_bouncie",
        session: Optional[ClientSession] = None,
    ) -> None:
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_url: str = redirect_url
        self._auth_code: str = auth_code
        self._state: str = state
        self._session: ClientSession = session
        self._access_token: str = None
        self._access_token_valid: bool = False
        self._user_email: str = None
        self._user_name: str = None
        self._user_id: str = None
        self._vehicles: list = []

    async def _handle_response(self, response):
        if response.status in (200, 201):
            data = await response.json()
        elif response.status == 400:
            raise BadRequestError(response.json()["errors"])
        elif response.status == 401:
            raise UnauthorizedError()
        elif response.status == 403:
            data = response.json()
            raise ForbiddenError(f"{data['error']} - {data['error_description']}")
        elif response.status == 404:
            raise NotFoundError()
        else:
            raise InternalError(response=response)
        return data

    async def _post(
        self, endpoint: str, data: dict, base_url: str = REST_API_BASE_URL
    ) -> list:
        current_session = self._session and not self._session.closed

        session: ClientSession = None
        if current_session:
            session = self._session
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT_SECONDS)
            )

        try:
            async with session.post(f"{base_url}/{endpoint}", data=data) as response:
                data = await self._handle_response(response=response)
        except UnauthorizedError:
            self.get_access_token()
            self._post(base_url=base_url, endpoint=endpoint, data=data)
        finally:
            if not current_session:
                await session.close()
        return data

    async def _get(self, base_url: str, endpoint: str, **kwargs) -> list:
        current_session = self._session and not self._session.closed
        session: ClientSession = None
        data = None
        if current_session:
            session = self._session
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT_SECONDS)
            )
        try:
            async with session.get(f"{base_url}/{endpoint}", **kwargs) as response:
                data = await self._handle_response(response=response)
        except UnauthorizedError:
            self.get_access_token()
            self._get(base_url=base_url, endpoint=endpoint, **kwargs)
        finally:
            if not current_session:
                await session.close()
        return data

    async def get_access_token(self):
        data = await self._post(
            endpoint="",
            base_url=AUTH_TOKEN_URL,
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": AUTH_GRANT_TYPE,
                "code": self._auth_code,
                "redirect_uri": self._redirect_url,
            },
        )
        self._access_token = data["access_token"]
        self._access_token_valid = True
        return data["access_token"]

    async def search_for_trips(
        self,
        imei: str,
        gps_format: str,
        transaction_id: str = None,
        starts_after=None,
        ends_before=None,
    ):
        pass

    async def get_user(self):
        data = await self._get(base_url=REST_API_BASE_URL, endpoint="user")
        self._user_name = data["name"] if "name" in data else None
        self._user_email = data["email"] if "email" in data else None
        self._user_id = data["id"] if "id" in data else None
        return data

    async def get_all_vehicles(self):
        data = await self._get(base_url=REST_API_BASE_URL, endpoint="vehicles")
        self._vehicles = data
        return data

    async def get_vehicles(self, imei: str = None, vin: str = None):
        params = {}
        if vin:
            params["vin"] = vin
        elif imei:
            params["imei"] = imei
        else:
            return await self.get_all_vehicles()
        data = await self._get(
            base_url=REST_API_BASE_URL, endpoint="vehicles", params=params
        )
        return data
