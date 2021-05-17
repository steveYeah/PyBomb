"""Tests for all PyBomb Search Clients."""
import importlib
import re
from typing import Any
from unittest.mock import MagicMock

import pkg_resources
import pytest
from requests.exceptions import HTTPError

from pybomb.clients.base.search_client import SearchClient
from pybomb.exceptions import (
    BadRequestException,
    InvalidFilterFieldException,
    InvalidResponseException,
    InvalidReturnFieldException,
    InvalidSortFieldException,
)
from pybomb.response import Response

version = pkg_resources.require("pybomb")[0].version
client_pattern = re.compile(r"(?<!^)(?=[A-Z])")

# TODO: Needs to move to a YAML file for editing by code
test_clients = [
    "PlatformsClient",
    "GamesClient",
]


@pytest.mark.parametrize("test_client", test_clients)
class TestSearchClients:
    """Tests and fixtures for the Clients."""

    @pytest.fixture
    def search_client(
        self, test_client: str, mock_response: MagicMock, mock_requests_get: MagicMock,
    ) -> SearchClient:
        """Test mock SearchClient.

        Will mock request to GB API.
        """
        client_module_name = client_pattern.sub("_", test_client).lower()
        client_module = importlib.import_module(f"pybomb.clients.{client_module_name}")
        test_client_class = getattr(client_module, test_client)

        mock_requests_get.return_value = mock_response
        search_client = test_client_class("fake_key")

        return search_client

    @pytest.mark.parametrize(
        "search_method, call_params",
        (("quick_search", "Something"), ("search", {"name": "Something"})),
    )
    def test_bad_giantbomb_request(
        self,
        search_method: str,
        call_params: Any,
        search_client: SearchClient,
        mock_response: MagicMock,
    ) -> None:
        """Test bad request errors are correctly handled."""
        mock_response.raise_for_status.side_effect = HTTPError("Test error")

        with pytest.raises(BadRequestException):
            getattr(search_client, search_method)(call_params)

    @pytest.mark.parametrize(
        "search_method, call_params",
        (("quick_search", "Something"), ("search", {"name": "Something"})),
    )
    def test_bad_giantbomb_response(
        self,
        search_method: str,
        call_params: Any,
        search_client: SearchClient,
        mock_response: MagicMock,
    ) -> None:
        """Test bad response errors are correctly handled."""
        mock_response_json = mock_response.json()
        mock_response_json["status_code"] = 2
        mock_response_json["error"] = "Badness"
        mock_response.json.return_value = mock_response_json

        with pytest.raises(InvalidResponseException):
            getattr(search_client, search_method)(call_params)

    class TestGeneral:
        """General tests for the client across methods."""

        def test_use_json_return_format(
            self, search_client: SearchClient, mock_requests_get: MagicMock,
        ) -> None:
            """Test JSON format is used in GB API call."""
            res = search_client.quick_search("name")
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

    class TestQuickSearch:
        """Tests for the quick_search method."""

        def test_search(
            self,
            search_client: SearchClient,
            mock_response: MagicMock,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test response and API call are as expected."""
            res = search_client.quick_search("name")

            assert isinstance(res, Response)
            assert res.uri == mock_response.url

            mock_response_json = mock_response.json()
            assert res.results == mock_response_json["results"]
            assert res.result is None

            assert res.num_page_results == (
                mock_response_json["number_of_page_results"]
            )

            assert res.num_total_results == (
                mock_response_json["number_of_total_results"]
            )

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
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
            search_client: SearchClient,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test search with sort order and direction."""
            res = search_client.quick_search(
                "name", sort_by="date_added", desc=sort_dec
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "sort": "date_added:{0}".format(sort_direction),
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invaild_sort(self, search_client: SearchClient) -> None:
            """Test use of invalid sort field is caught and handled correctly."""
            with pytest.raises(InvalidSortFieldException):
                search_client.quick_search("name", sort_by="aliases")

    class TestSearch:
        """Test full seach method."""

        def test_filter_search(
            self,
            search_client: SearchClient,
            mock_response: MagicMock,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test search filters are applied to GB API call."""
            res = search_client.search({"name": "name"})

            assert isinstance(res, Response)
            assert res.uri == mock_response.url

            mock_response_json = mock_response.json()
            assert res.results == mock_response_json["results"]
            assert res.result is None

            assert res.num_page_results == (
                mock_response_json["number_of_page_results"]
            )

            assert res.num_total_results == (
                mock_response_json["number_of_total_results"]
            )

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invalid_filters(self, search_client: SearchClient) -> None:
            """Test use of invalid filters are caught and handled correctly."""
            with pytest.raises(InvalidFilterFieldException):
                search_client.search({"api_detail_url": "something"})

        def test_can_specify_return_fields(
            self, search_client: SearchClient, mock_requests_get: MagicMock
        ) -> None:
            """Test return fields are applied to GB API call correctly."""
            res = search_client.search({"name": "name"}, return_fields=["id", "name"])
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "field_list": "id,name",
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invalid_return_fields(self, search_client: SearchClient) -> None:
            """Test use of invalid return fields are caught and handled correctly."""
            with pytest.raises(InvalidReturnFieldException):
                search_client.search({"name": "name"}, return_fields=["bad"])

        @pytest.mark.parametrize(
            "sort_dec, sort_direction", [(True, "desc"), (False, "asc")]
        )
        def test_sort(
            self,
            sort_dec: bool,
            sort_direction: str,
            search_client: SearchClient,
            mock_requests_get: MagicMock,
        ) -> None:
            """Test sort field is applied to GB API call correctly."""
            res = search_client.search(
                {"name": "name"}, sort_by="date_added", desc=sort_dec
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "sort": "date_added:{0}".format(sort_direction),
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_invaild_sort(self, search_client: SearchClient) -> None:
            """Test use of invalid sort field is caught and handled correctly."""
            with pytest.raises(InvalidSortFieldException):
                search_client.search({"name": "name"}, sort_by="company")

        def test_limit(
            self, search_client: SearchClient, mock_requests_get: MagicMock
        ) -> None:
            """Test return limit is applied to GB API call correctly."""
            res = search_client.search({"name": "name"}, limit=1)
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "limit": 1,
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )

        def test_offset(
            self, search_client: SearchClient, mock_requests_get: MagicMock
        ) -> None:
            """Test offset is applied to GB API call correctly."""
            res = search_client.search({"name": "name"}, offset=10)
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                f"http://www.giantbomb.com/api/{search_client.RESOURCE_NAME}",
                params={
                    "filter": "name:name",
                    "offset": 10,
                    "api_key": "fake_key",
                    "format": "json",
                },
                headers={"User-Agent": "Pybomb {}".format(version)},
            )
