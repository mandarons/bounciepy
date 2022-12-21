from aiohttp import ClientSession, ClientTimeout
from typing import Optional

from bounciepy.const import (
    REST_API_BASE_URL,
    AUTH_TOKEN_URL,
    AUTH_GRANT_TYPE,
    API_DEFAULT_TIMEOUT_SECONDS,
)
from bounciepy.exceptions import (
    BadRequestError,
    UnauthorizedError,
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
        self._headers: dict = {}

    @property
    def client_session(self):
        return self._session

    @property
    def access_token(self):
        return self._access_token

    def _set_access_token(self, access_token):
        self._access_token = access_token
        self._headers = {"Authorization": access_token}
        self._access_token_valid = True

    async def _handle_response(self, response):
        data = None
        if response.status in (200, 201):
            data = await response.json()
        elif response.status == 400:
            data = await response.json()
            raise BadRequestError(data["errors"])
        elif response.status == 401:
            self._access_token_valid = False
            raise UnauthorizedError("Error: Invalid or expired access token.")
        return data

    async def _get_session(self):
        if not self._session or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT_SECONDS)
            )
        return self._session

    async def get_access_token(self):
        current_session = await self._get_session()
        async with current_session.post(
            url=AUTH_TOKEN_URL,
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": AUTH_GRANT_TYPE,
                "code": self._auth_code,
                "redirect_uri": self._redirect_url,
            },
        ) as response:
            data = await self._handle_response(response=response)
            self._set_access_token(access_token=data["access_token"])
        return True

    async def http_get(self, url, **kwargs):
        count = 0
        while count < 2:
            try:
                current_session = await self._get_session()
                response = await current_session.get(
                    url=url, headers=self._headers, **kwargs
                )
                data = await self._handle_response(response=response)
                count = 2
            except UnauthorizedError:
                if await self.get_access_token():
                    count = 1
        return data

    async def get_user(self):
        user_data = await self.http_get(f"{REST_API_BASE_URL}/user")
        self._user_name = user_data["name"] if "name" in user_data else None
        self._user_email = user_data["email"] if "email" in user_data else None
        self._user_id = user_data["id"] if "id" in user_data else None
        return user_data

    async def get_all_vehicles(self):
        vehicles_data = await self.http_get(f"{REST_API_BASE_URL}/vehicles")
        self._vehicles = vehicles_data
        return vehicles_data

    async def get_vehicle_by_imei(self, imei):
        vehicle_data = await self.http_get(
            f"{REST_API_BASE_URL}/vehicles",
            params={"imei": imei},
        )
        return vehicle_data[0]

    async def get_vehicle_by_vin(self, vin):
        vehicle_data = await self.http_get(
            url=f"{REST_API_BASE_URL}/vehicles",
            params={"vin": vin},
        )
        return vehicle_data[0]

    async def search_for_trips(
        self, imei, gps_format, transaction_id=None, starts_after=None, ends_before=None
    ):
        params = {"imei": imei, "gps-format": gps_format}
        # TODO use transaction_id, starts_after and ends_before params
        trip_data = await self.http_get(f"{REST_API_BASE_URL}/trips", params=params)
        return trip_data
