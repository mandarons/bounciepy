from typing import Optional, Union

from aiohttp import ClientResponse, ClientSession, ClientTimeout

from bounciepy.const import (
    API_DEFAULT_TIMEOUT_SECONDS,
    AUTH_GRANT_TYPE,
    AUTH_TOKEN_URL,
    REST_API_BASE_URL,
)
from bounciepy.exceptions import BadRequestError, UnauthorizedError


class AsyncRESTAPIClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        auth_code: str,
        state: str = "init_bouncie",
        session: Optional[ClientSession] = None,
    ) -> None:
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_url: str = redirect_url
        self._auth_code: str = auth_code
        self._state: str = state
        self._session: Optional[ClientSession] = session
        self._access_token: Optional[str] = None
        self._access_token_valid: bool = False
        self._user_email: Optional[str] = None
        self._user_name: Optional[str] = None
        self._user_id: Optional[str] = None
        self._vehicles: list = []
        self._headers: dict = {}

    @property
    def client_session(self) -> Optional[ClientSession]:
        return self._session

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    def _set_access_token(self, access_token: str) -> None:
        self._access_token = access_token
        self._headers = {"Authorization": access_token}
        self._access_token_valid = True

    async def _handle_response(
        self, response: ClientResponse
    ) -> Union[dict, list, None]:
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

    async def _get_session(self) -> ClientSession:
        if not self._session or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT_SECONDS)
            )
        return self._session

    async def get_access_token(self) -> bool:
        current_session = await self._get_session()
        data: dict = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": AUTH_GRANT_TYPE,
            "code": self._auth_code,
            "redirect_uri": self._redirect_url,
        }
        async with current_session.post(
            url=AUTH_TOKEN_URL,
            data=data,
        ) as response:
            response_data = await self._handle_response(response)
            if not response_data:
                return False
            if isinstance(response_data, dict):
                self._set_access_token(access_token=response_data["access_token"])
        return True

    async def http_get(self, url: str, **kwargs: dict) -> Union[dict, list, None]:
        count = 0
        while count < 2:
            try:
                current_session = await self._get_session()
                response = await current_session.get(
                    url=url, headers=self._headers, allow_redirects=True, **kwargs
                )
                data = await self._handle_response(response)
                count = 2
            except UnauthorizedError:
                if await self.get_access_token():
                    count = 1
        return data

    async def get_user(self) -> Optional[dict]:
        user_data = await self.http_get(f"{REST_API_BASE_URL}/user")
        if user_data and isinstance(user_data, dict):
            self._user_name = user_data["name"] if "name" in user_data else None
            self._user_email = user_data["email"] if "email" in user_data else None
            self._user_id = user_data["id"] if "id" in user_data else None
            return user_data
        return None

    async def get_all_vehicles(self) -> Optional[list]:
        vehicles_data = await self.http_get(f"{REST_API_BASE_URL}/vehicles")
        if vehicles_data and isinstance(vehicles_data, list):
            self._vehicles = vehicles_data
            return vehicles_data
        return None

    async def get_vehicle_by_imei(self, imei: str) -> Optional[dict]:
        vehicle_data = await self.http_get(
            f"{REST_API_BASE_URL}/vehicles",
            params={"imei": imei},
        )
        if isinstance(vehicle_data, list):
            return vehicle_data[0]
        return None

    async def get_vehicle_by_vin(self, vin):
        vehicle_data = await self.http_get(
            url=f"{REST_API_BASE_URL}/vehicles",
            params={"vin": vin},
        )
        if isinstance(vehicle_data, list):
            return vehicle_data[0]
        return None

    async def get_trips(self, imei: str, gps_format: str="geojson") -> Optional[list]:
        trip_data = await self.http_get(
            f"{REST_API_BASE_URL}/trips",
            params={"imei": imei,
                    "gps-format": gps_format},
        )
        if trip_data and isinstance(trip_data, list):
            return trip_data
        return None
