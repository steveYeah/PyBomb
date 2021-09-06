"""Tests for the PyBomb FetchClient."""
import importlib
import re
from typing import Generator
from unittest.mock import MagicMock, patch

import pkg_resources
import pytest
from requests.exceptions import HTTPError
from requests.models import Response as RequestsResponse

from pybomb.clients.base.fetch_client import FetchClient
from pybomb.exceptions import (
    BadRequestException,
    InvalidResponseException,
    InvalidReturnFieldException,
)
from pybomb.response import Response
from .helpers import get_clients


version = pkg_resources.require("pybomb")[0].version
client_pattern = re.compile(r"(?<!^)(?=[A-Z])")

test_clients = get_clients("fetch_client")


@pytest.mark.parametrize("test_client", test_clients)
class TestFetchClients:
    """Tests and fixtures for the FetchClient."""

    @pytest.fixture
    def mock_requests_get(self) -> Generator[MagicMock, None, None]:
        """Request GET test mock."""
        with patch("pybomb.clients.base.fetch_client.get") as req_mock:
            yield req_mock

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        """Raw response test mock."""
        mock_response = MagicMock(RequestsResponse)
        mock_response.url = "https://fake.com"

        mock_response.json.return_value = {
            "status_code": 1,
            "number_of_page_results": 1,
            "number_of_total_results": 1,
            "results": {"id": 1, "description": "Great Game"},
        }

        return mock_response

    @pytest.fixture
    def fetch_client(
        self,
        test_client: MagicMock,
        mock_response: MagicMock,
        mock_requests_get: MagicMock,
    ) -> FetchClient:
        """Test mock FetchClient.

        Will mock request to GB API.
        """
        client_module_name = client_pattern.sub("_", test_client).lower()
        client_module = importlib.import_module(f"pybomb.clients.{client_module_name}")
        test_client_class = getattr(client_module, test_client)

        mock_requests_get.return_value = mock_response
        fetch_client = test_client_class("fake_key")

        return fetch_client

    def test_fetch(
        self,
        fetch_client: FetchClient,
        mock_response: MagicMock,
        mock_requests_get: MagicMock,
    ) -> None:
        """Test the fetch method.

        Check the call and response to/from GB API was correct.
        """
        res = fetch_client.fetch(1)

        assert isinstance(res, Response)
        assert res.uri == mock_response.url

        mock_response_json = mock_response.json()
        assert res.results == [mock_response_json["results"]]
        assert res.result == mock_response_json["results"]

        assert res.num_page_results == (mock_response_json["number_of_page_results"])

        assert res.num_total_results == (mock_response_json["number_of_total_results"])

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"api_key": "fake_key", "format": "json"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_use_json_return_format(
        self,
        fetch_client: FetchClient,
        mock_response: MagicMock,
        mock_requests_get: MagicMock,
    ) -> None:
        """Test JSON response format is used in GB API call."""
        res = fetch_client.fetch(1)
        assert isinstance(res, Response)

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"api_key": "fake_key", "format": "json"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_can_specify_return_fields(
        self, fetch_client: FetchClient, mock_requests_get: MagicMock
    ) -> None:
        """Test return fields are used and formatted correctly in GB API call."""
        res = fetch_client.fetch(1, ["id", "name"])
        assert isinstance(res, Response)

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"field_list": "id,name", "api_key": "fake_key", "format": "json"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_invalid_return_fields(self, fetch_client: FetchClient) -> None:
        """Test return fields are correctly validated."""
        with pytest.raises(InvalidReturnFieldException):
            fetch_client.fetch(1, ["bad", "params"])

    def test_bad_giantbomb_request(
        self, fetch_client: FetchClient, mock_response: MagicMock
    ) -> None:
        """Test bad request errors are correctly handled."""
        mock_response.raise_for_status.side_effect = HTTPError("Test error")

        with pytest.raises(BadRequestException):
            fetch_client.fetch(1)

    def test_bad_giantbomb_response(
        self, fetch_client: FetchClient, mock_response: MagicMock
    ) -> None:
        """Test bad response errors are correctly handled."""
        mock_response_json = mock_response.json()
        mock_response_json["status_code"] = 2
        mock_response_json["error"] = "Badness"
        mock_response.json.return_value = mock_response_json

        with pytest.raises(InvalidResponseException):
            fetch_client.fetch(1)
