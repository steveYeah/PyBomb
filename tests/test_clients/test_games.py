"""Tests for the PyBomb GamesClient."""
from typing import Any
from unittest.mock import MagicMock, patch

import pkg_resources
import pytest
from requests.exceptions import HTTPError
from requests.models import Response as RequestsResponse

import pybomb
from pybomb.clients.games_client import GamesClient
from pybomb.exceptions import (
    BadRequestException,
    InvalidFilterFieldException,
    InvalidResponseException,
    InvalidReturnFieldException,
    InvalidSortFieldException,
)
from pybomb.response import Response


version = pkg_resources.require("pybomb")[0].version


class TestGamesClient:
    """Tests and fixtures for the GamesClient."""

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
            "results": [{"id": 1, "description": "Great Game"}],
        }

        return mock_response

    @pytest.fixture
    def games_client(
        self, mock_response: MagicMock, mock_requests_get: MagicMock
    ) -> GamesClient:
        """Test mock GamesClient.

        Will mock request to GB API.
        """
        mock_requests_get.return_value = mock_response
        games_client = GamesClient("fake_key")

        return games_client

    @pytest.mark.parametrize(
        "search_method, call_params",
        (("quick_search", "a game"), ("search", {"name": "a game"})),
    )
    def test_bad_giantbomb_request(
        self,
        search_method: str,
        call_params: Any,
        games_client: GamesClient,
        mock_response: MagicMock,
    ) -> None:
        """Test bad request errors are correctly handled."""
        mock_response.raise_for_status.side_effect = HTTPError("Test error")

        with pytest.raises(BadRequestException):
            getattr(games_client, search_method)(call_params)

    @pytest.mark.parametrize(
        "search_method, call_params",
        (("quick_search", "a game"), ("search", {"name": "a game"})),
    )
    def test_bad_giantbomb_response(
        self,
        search_method: str,
        call_params: Any,
        games_client: GamesClient,
        mock_response: MagicMock,
    ) -> None:
        """Test bad response errors are correctly handled."""
        mock_response_json = mock_response.json()
        mock_response_json["status_code"] = 2
        mock_response_json["error"] = "Badness"
        mock_response.json.return_value = mock_response_json

        with pytest.raises(InvalidResponseException):
            getattr(games_client, search_method)(call_params)

    class TestGeneral:
        """General tests for the client across methods."""

        def test_use_given_return_format(
            self, games_client: GamesClient, mock_requests_get: MagicMock
        ) -> None:
            """Test response format is used in GB API call."""
            games_client.default_format = games_client.RESPONSE_FORMAT_XML

            res = games_client.quick_search("game name")
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "api_key": "fake_key",
                    "format": "xml",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

    class TestQuickSearch:
        """Tests for the quick_search method."""

        def test_search(
            self,
            games_client: GamesClient,
            mock_response: MagicMock,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test response and API call are as expected."""
            res = games_client.quick_search("game name")

            assert isinstance(res, Response)
            assert res.uri == mock_response.url

            mock_response_json = mock_response.json()
            assert res.results == mock_response_json["results"]

            assert res.num_page_results == (
                mock_response_json["number_of_page_results"]
            )

            assert res.num_total_results == (
                mock_response_json["number_of_total_results"]
            )

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_search_with_platform(
            self, games_client: GamesClient, mock_requests_get: MagicMock
        ) -> None:
            """Test search with a platform filter."""
            res = games_client.quick_search("game name", pybomb.PS1)

            assert isinstance(res, Response)
            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": f"name:game name,platforms:{pybomb.PS1}",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        @pytest.mark.parametrize(
            "sort_dec, sort_direction", [(True, "desc"), (False, "asc")]
        )
        def test_sort(
            self,
            sort_dec: bool,
            sort_direction: str,
            games_client: GamesClient,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test search with sort order and direction."""
            res = games_client.quick_search(
                "game name", sort_by="date_added", desc=sort_dec
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "sort": "date_added:{0}".format(sort_direction),
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invaild_sort(self, games_client: GamesClient) -> None:
            """Test use of invalid sort field is caught and handled correctly."""
            with pytest.raises(InvalidSortFieldException):
                games_client.quick_search("game name", sort_by="aliases")

    class TestSearch:
        """Test full seach method."""

        def test_filter_search(
            self,
            games_client: GamesClient,
            mock_response: MagicMock,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test search filters are applied to GB API call."""
            res = games_client.search({"name": "game name"})

            assert isinstance(res, Response)
            assert res.uri == mock_response.url

            mock_response_json = mock_response.json()
            assert res.results == mock_response_json["results"]

            assert res.num_page_results == (
                mock_response_json["number_of_page_results"]
            )

            assert res.num_total_results == (
                mock_response_json["number_of_total_results"]
            )

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invalid_filters(self, games_client: GamesClient) -> None:
            """Test use of invalid filters are caught and handled correctly."""
            with pytest.raises(InvalidFilterFieldException):
                games_client.search({"image": "image_file_name.jpg"})

        def test_can_specify_return_fields(
            self, games_client: GamesClient, mock_requests_get: MagicMock
        ) -> None:
            """Test return fields are applied to GB API call correctly."""
            res = games_client.search(
                {"name": "game name"}, return_fields=["id", "name"]
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "field_list": "id,name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invalid_return_fields(self, games_client: GamesClient) -> None:
            """Test use of invalid return fields are caught and handled correctly."""
            with pytest.raises(InvalidReturnFieldException):
                games_client.search({"name": "game name"}, return_fields=["bad"])

        @pytest.mark.parametrize(
            "sort_dec, sort_direction", [(True, "desc"), (False, "asc")]
        )
        def test_sort(
            self,
            sort_dec: bool,
            sort_direction: str,
            games_client: GamesClient,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test sort field is applied to GB API call correctly."""
            res = games_client.search(
                {"name": "game name"}, sort_by="date_added", desc=sort_dec
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "sort": "date_added:{0}".format(sort_direction),
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invaild_sort(self, games_client: GamesClient) -> None:
            """Test use of invalid sort field is caught and handled correctly."""
            with pytest.raises(InvalidSortFieldException):
                games_client.search({"name": "game name"}, sort_by="aliases")

        def test_limit(
            self, games_client: GamesClient, mock_requests_get: MagicMock
        ) -> None:
            """Test return limit is applied to GB API call correctly."""
            res = games_client.search({"name": "game name"}, limit=1)
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "limit": 1,
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_offset(
            self, games_client: GamesClient, mock_requests_get: MagicMock
        ) -> None:
            """Test offset is applied to GB API call correctly."""
            res = games_client.search({"name": "game name"}, offset=10)
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                "http://www.giantbomb.com/api/games",
                params={
                    "filter": "name:game name",
                    "offset": 10,
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )
