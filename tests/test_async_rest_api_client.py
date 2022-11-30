import pytest
from bounciepy import AsyncRESTAPIClient
from tests.const import (
    MOCK_ACCESS_TOKEN,
    MOCK_CLIENT_ID,
    MOCK_CLIENT_SECRET,
    MOCK_REDIRECT_URI,
    MOCK_AUTH_CODE,
    MOCK_USER_RESPONSE,
    MOCK_VEHICLES_RESPONSE,
)


def get_client():
    return AsyncRESTAPIClient(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        redirect_url=MOCK_REDIRECT_URI,
        auth_code=MOCK_AUTH_CODE,
    )


@pytest.mark.asyncio
async def test_get_access_token(client):
    data = await client.get_access_token()
    assert data is True
    assert client.access_token == MOCK_ACCESS_TOKEN


@pytest.mark.asyncio
async def test_get_user(client):
    assert True is await client.get_access_token()
    data = await client.get_user()
    assert data["id"] == MOCK_USER_RESPONSE[0]["id"]


@pytest.mark.asyncio
async def test_get_all_vehicles(client):
    assert True is await client.get_access_token()
    data = await client.get_all_vehicles()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_imei(client):
    assert True is await client.get_access_token()
    data = await client.get_vehicle_by_imei(imei=MOCK_VEHICLES_RESPONSE[0]["imei"])
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_vin(client):
    assert True is await client.get_access_token()
    data = await client.get_vehicle_by_vin(vin=MOCK_VEHICLES_RESPONSE[0]["vin"])
    assert len(data) > 0
