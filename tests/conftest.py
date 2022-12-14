"""Tests configuration."""
import asyncio
import re

import pytest
from aioresponses import aioresponses

from bounciepy import AsyncRESTAPIClient
from bounciepy.const import AUTH_TOKEN_URL, REST_API_BASE_URL
from tests.const import (
    MOCK_AUTH_CODE,
    MOCK_CLIENT_ID,
    MOCK_CLIENT_SECRET,
    MOCK_REDIRECT_URI,
)
from tests.mock_responses import mock_response


# pylint: disable=W0621
@pytest.fixture
def event_loop():
    """Get event loop."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client(event_loop):
    """Get http client."""
    with aioresponses() as mock_aioresponse:
        mock_aioresponse.post(re.compile(f"{AUTH_TOKEN_URL}/*"), callback=mock_response)
        mock_aioresponse.get(
            re.compile(f"{REST_API_BASE_URL}/*"), callback=mock_response
        )
        mock_aioresponse.get(
            re.compile(f"{REST_API_BASE_URL}/*"), callback=mock_response
        )
        client = AsyncRESTAPIClient(
            client_id=MOCK_CLIENT_ID,
            client_secret=MOCK_CLIENT_SECRET,
            redirect_url=MOCK_REDIRECT_URI,
            auth_code=MOCK_AUTH_CODE,
        )
        yield client
        event_loop.run_until_complete(client.client_session.close())
