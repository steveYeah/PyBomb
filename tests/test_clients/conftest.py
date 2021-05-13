"""Shared fixtures."""
from unittest.mock import MagicMock, patch

import pytest
from requests.models import Response as RequestsResponse


@pytest.fixture
def mock_requests_get() -> MagicMock:
    """Request GET test mock."""
    with patch("pybomb.clients.base.search_client.get") as req_mock:
        yield req_mock


@pytest.fixture
def mock_response() -> MagicMock:
    """Raw response test mock."""
    mock_response = MagicMock(RequestsResponse)
    mock_response.url = "https://fake.com"

    mock_response.json.return_value = {
        "status_code": 1,
        "number_of_page_results": 1,
        "number_of_total_results": 1,
        "results": [],
    }

    return mock_response
