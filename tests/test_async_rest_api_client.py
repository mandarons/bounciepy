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
async def test_get_access_token(mock_bouncie_api):
    print(mock_bouncie_api)
    client = get_client()
    data = await client.get_access_token()
    assert data == MOCK_ACCESS_TOKEN


@pytest.mark.asyncio
async def test_get_user(mock_bouncie_api):
    client = get_client()
    data = await client.get_user()
    assert data[0]["id"] == MOCK_USER_RESPONSE[0]["id"]


@pytest.mark.asyncio
async def test_get_all_vehicles(mock_bouncie_api):
    client = get_client()
    data = await client.get_all_vehicles()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_imei(mock_bouncie_api):
    client = get_client()
    data = await client.get_vehicles(imei=MOCK_VEHICLES_RESPONSE[0]["imei"])
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_vin(mock_bouncie_api):
    client = get_client()
    data = await client.get_vehicles(vin=MOCK_VEHICLES_RESPONSE[0]["vin"])
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles(mock_bouncie_api):
    client = get_client()
    data = await client.get_vehicles()
    assert len(data) > 0
