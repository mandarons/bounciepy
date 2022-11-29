import pytest
import re
from aioresponses import aioresponses
from tests.mock_responses import mock_response
from bounciepy.const import AUTH_TOKEN_URL, REST_API_BASE_URL

# pylint: disable=W0621
@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
def mock_bouncie_api(mock_aioresponse):
    mock_aioresponse.post(re.compile(f"{AUTH_TOKEN_URL}/*"), callback=mock_response)
    mock_aioresponse.get(re.compile(f"{REST_API_BASE_URL}/*"), callback=mock_response)
