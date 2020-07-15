"""Tests for the PyBomb GameClient."""
from unittest.mock import MagicMock, patch

import pkg_resources
import pytest
from requests.exceptions import HTTPError
from requests.models import Response as RequestsResponse

from pybomb.clients.game_client import GameClient
from pybomb.exceptions import (
    BadRequestException,
    InvalidResponseException,
    InvalidReturnFieldException,
)
from pybomb.response import Response


version = pkg_resources.require("pybomb")[0].version


class TestGameClient:
    """Tests and fixtures for the GameClient."""

    @pytest.fixture
    def mock_requests_get(self) -> MagicMock:
        """Request GET test mock."""
        with patch("pybomb.clients.base_client.get") as req_mock:
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
    def game_client(
        self, mock_response: MagicMock, mock_requests_get: MagicMock
    ) -> GameClient:
        """Test mock GameClient.

        Will mock request to GB API.
        """
        mock_requests_get.return_value = mock_response
        game_client = GameClient("fake_key")

        return game_client

    def test_can_fetch_game(
        self,
        game_client: GameClient,
        mock_response: MagicMock,
        mock_requests_get: MagicMock,
    ) -> None:
        """Test the fetch method.

        Check the reponse and call to GB API was correct.
        """
        res = game_client.fetch(1)

        assert isinstance(res, Response)
        assert res.uri == mock_response.url

        mock_response_json = mock_response.json()
        assert res.results == mock_response_json["results"]

        assert res.num_page_results == (mock_response_json["number_of_page_results"])

        assert res.num_total_results == (mock_response_json["number_of_total_results"])

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"api_key": "fake_key", "format": "json"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_use_given_return_format(
        self,
        game_client: GameClient,
        mock_response: MagicMock,
        mock_requests_get: MagicMock,
    ) -> None:
        """Test response format is used in GB API call."""
        game_client.default_format = game_client.RESPONSE_FORMAT_XML
        res = game_client.fetch(1)
        assert isinstance(res, Response)

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"api_key": "fake_key", "format": "xml"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_can_specify_return_fields(
        self, game_client: GameClient, mock_requests_get: MagicMock
    ) -> None:
        """Test return fields are used and formatted correctly in GB API call."""
        res = game_client.fetch(1, ("id", "name"))
        assert isinstance(res, Response)

        mock_requests_get.assert_called_once_with(
            "http://www.giantbomb.com/api/game/1",
            params={"field_list": "id,name", "api_key": "fake_key", "format": "json"},
            headers={"User-Agent": "Pybomb {}".format(version)},
        )

    def test_invalid_return_fields(self, game_client: GameClient) -> None:
        """Test return fields are correctly validated."""
        with pytest.raises(InvalidReturnFieldException):
            game_client.fetch(1, ("bad", "params"))

    def test_bad_giantbomb_request(
        self, game_client: GameClient, mock_response: MagicMock
    ) -> None:
        """Test bad request errors are correctly handled."""
        mock_response.raise_for_status.side_effect = HTTPError("Test error")

        with pytest.raises(BadRequestException):
            game_client.fetch(1)

    def test_bad_giantbomb_response(
        self, game_client: GameClient, mock_response: MagicMock
    ) -> None:
        """Test bad response errors are correctly handled."""
        mock_response_json = mock_response.json()
        mock_response_json["status_code"] = 2
        mock_response_json["error"] = "Badness"
        mock_response.json.return_value = mock_response_json

        with pytest.raises(InvalidResponseException):
            game_client.fetch(1)
