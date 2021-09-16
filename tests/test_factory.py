"""Test the factory module."""
import pytest

from pybomb.clients.games_client import GamesClient
from pybomb.exceptions import InvalidClientException
from pybomb.factory import ClientFactory


class TestClientFactory:
    """Test the ClientFactory."""

    def test_return_specified_factory(self) -> None:
        """Test the factory returns the requested client.

        Client should be created with the expected API key.
        """
        test_key = "12345"
        client = ClientFactory(test_key).build("games")

        assert isinstance(client, GamesClient)
        assert client.api_key == test_key

    def test_raise_on_invalid_client(self) -> None:
        """Test an exception is raised when client not found."""
        with pytest.raises(InvalidClientException):
            ClientFactory("1234").build("invalid_client")
