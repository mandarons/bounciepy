import pytest
from bounciepy import exceptions
from tests.const import (
    MOCK_ACCESS_TOKEN,
    MOCK_USER_RESPONSE,
    MOCK_VEHICLES_RESPONSE,
)


@pytest.mark.asyncio
async def test_get_access_token(client):
    data = await client.get_access_token()
    assert data is True
    assert client.access_token == MOCK_ACCESS_TOKEN


@pytest.mark.asyncio
async def test_unauthorized(client):
    # pylint: disable=W0212
    token = client._access_token
    # pylint: disable=W0212
    client._set_access_token(access_token="invalid")
    with pytest.raises(exceptions.UnauthorizedError) as ex_info:
        await client.get_user()
        print(ex_info)
    # pylint: disable=W0212
    client._set_access_token(access_token=token)


@pytest.mark.asyncio
async def test_400_error(client):
    with pytest.raises(exceptions.BadRequestError) as ex_info:
        await client.get_user()
    print(ex_info)


@pytest.mark.asyncio
async def test_get_user(client):
    assert True is await client.get_access_token()
    data = await client.get_user()
    assert data["id"] == MOCK_USER_RESPONSE["id"]


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


@pytest.mark.asyncio
async def test_search_for_trips(client):
    assert True is await client.get_access_token()
    data = await client.search_for_trips(
        imei=MOCK_VEHICLES_RESPONSE[0]["imei"], gps_format="polyline"
    )
    assert len(data) > 0
