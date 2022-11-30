from aiohttp import ClientSession, ClientTimeout
from typing import Optional

from bounciepy.const import (
    REST_API_BASE_URL,
    AUTH_TOKEN_URL,
    AUTH_GRANT_TYPE,
    API_DEFAULT_TIMEOUT_SECONDS,
)
from bounciepy.exceptions import (
    InternalError,
    NotFoundError,
    ForbiddenError,
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
            raise BadRequestError(response.json()["errors"])
        elif response.status == 401:
            self._access_token_valid = False
            raise UnauthorizedError("Error: Invalid or expired access token.")
        elif response.status == 403:
            data = response.json()
            raise ForbiddenError(f"{data['error']} - {data['error_description']}")
        elif response.status == 404:
            raise NotFoundError("Error: resource not found.")
        else:
            raise InternalError(response.text())
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

    async def get_user(self):
        current_session = await self._get_session()
        async with current_session.get(
            url=f"{REST_API_BASE_URL}/user",
            headers=self._headers,
        ) as response:
            data = await self._handle_response(response=response)
            user_data = data
            self._user_name = user_data["name"] if "name" in user_data else None
            self._user_email = user_data["email"] if "email" in user_data else None
            self._user_id = user_data["id"] if "id" in user_data else None
        return user_data

    async def get_all_vehicles(self):
        current_session = await self._get_session()
        async with current_session.get(
            url=f"{REST_API_BASE_URL}/vehicles",
            headers=self._headers,
        ) as response:
            vehicles_data = await self._handle_response(response=response)
            self._vehicles = vehicles_data
        return vehicles_data

    async def get_vehicle_by_imei(self, imei):
        current_session = await self._get_session()
        async with current_session.get(
            url=f"{REST_API_BASE_URL}/vehicles",
            params={"imei": imei},
            headers=self._headers,
        ) as response:
            vehicle_data = await self._handle_response(response=response)
            return vehicle_data[0]

    async def get_vehicle_by_vin(self, vin):
        current_session = await self._get_session()
        async with current_session.get(
            url=f"{REST_API_BASE_URL}/vehicles",
            params={"vin": vin},
            headers=self._headers,
        ) as response:
            vehicle_data = await self._handle_response(response=response)
            return vehicle_data[0]

    async def search_for_trips(
        self, imei, gps_format, transaction_id=None, starts_after=None, ends_before=None
    ):
        current_session = await self._get_session()
        params = {"imei": imei, "gps-format": gps_format}
        # TODO use transaction_id, starts_after and ends_before params
        async with current_session.get(
            url=f"{REST_API_BASE_URL}/trips", params=params, headers=self._headers
        ) as response:
            trip_data = await self._handle_response(response=response)
            return trip_data
