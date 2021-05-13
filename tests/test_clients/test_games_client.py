"""Tests for Games Clients."""
from unittest.mock import MagicMock

import pkg_resources

import pybomb
from pybomb.clients.games_client import GamesClient
from pybomb.response import Response

version = pkg_resources.require("pybomb")[0].version


class TestGamesClient:
    """GamesClient specific tests."""

    def test_search_with_platform(
        self, mock_requests_get: MagicMock, mock_response: MagicMock
    ) -> None:
        """Test search with a platform filter."""
        games_client = GamesClient("fake_key")
        mock_requests_get.return_value = mock_response

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
