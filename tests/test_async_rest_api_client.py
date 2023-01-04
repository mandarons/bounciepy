"""Tests for async rest api client."""
import pytest

from bounciepy import exceptions
from tests.const import MOCK_ACCESS_TOKEN, MOCK_USER_RESPONSE, MOCK_VEHICLES_RESPONSE


@pytest.mark.asyncio
async def test_get_access_token(client):
    """Test get access token returns success."""
    data = await client.get_access_token()
    assert data is True
    assert client.access_token == MOCK_ACCESS_TOKEN


async def mock_handle_response(*args):
    """Fake handle_response."""
    return None


@pytest.mark.asyncio
async def test_get_none_access_token(client, monkeypatch):
    """Test get access token returns None."""
    monkeypatch.setattr(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient._handle_response",
        mock_handle_response,
    )
    data = await client.get_access_token()
    assert data is False


@pytest.mark.asyncio
async def test_unauthorized_get_retry(client):
    """Test invalid token retry."""
    # pylint: disable=W0212
    token = client._access_token
    # pylint: disable=W0212
    client._set_access_token(access_token="invalid")
    data = await client.get_user()
    assert data["id"] == MOCK_USER_RESPONSE["id"]
    # pylint: disable=W0212
    client._set_access_token(access_token=token)


@pytest.mark.asyncio
async def test_400_error(client):
    """Test 400 HTTP error."""
    with pytest.raises(exceptions.BadRequestError) as ex_info:
        await client.get_user()
    print(ex_info)


@pytest.mark.asyncio
async def test_get_user(client):
    """Test get user returns success."""
    assert True is await client.get_access_token()
    data = await client.get_user()
    assert data["id"] == MOCK_USER_RESPONSE["id"]


@pytest.mark.asyncio
async def test_get_user_none(client, monkeypatch):
    """Test get user returns None."""
    monkeypatch.setattr(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient._handle_response",
        mock_handle_response,
    )
    data = await client.get_user()
    assert data is None


@pytest.mark.asyncio
async def test_get_all_vehicles(client):
    """Test get all vehicles returns success."""
    assert True is await client.get_access_token()
    data = await client.get_all_vehicles()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_all_vehicles_none(client, monkeypatch):
    """Test get all vehicles returns None."""
    monkeypatch.setattr(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient._handle_response",
        mock_handle_response,
    )
    data = await client.get_all_vehicles()
    assert data is None


@pytest.mark.asyncio
async def test_get_vehicles_by_imei(client):
    """Test get vehicles by imei returns success."""
    assert True is await client.get_access_token()
    data = await client.get_vehicle_by_imei(imei=MOCK_VEHICLES_RESPONSE[0]["imei"])
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_imei_none(client, monkeypatch):
    """Test get vehicles by imei returns None."""
    monkeypatch.setattr(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient._handle_response",
        mock_handle_response,
    )
    data = await client.get_vehicle_by_imei(imei=MOCK_VEHICLES_RESPONSE[0]["imei"])
    assert data is None


@pytest.mark.asyncio
async def test_get_vehicles_by_vin(client):
    """Test get vehicles by vin returns success."""
    assert True is await client.get_access_token()
    data = await client.get_vehicle_by_vin(vin=MOCK_VEHICLES_RESPONSE[0]["vin"])
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_vehicles_by_vin_none(client, monkeypatch):
    """Test get vehicles by vin that returns None."""
    monkeypatch.setattr(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient._handle_response",
        mock_handle_response,
    )
    data = await client.get_vehicle_by_vin(vin=MOCK_VEHICLES_RESPONSE[0]["vin"])
    assert data is None
