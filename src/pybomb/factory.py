"""Factories for creating Clients."""
from importlib import import_module

from pybomb.clients.base.client import Client
from pybomb.exceptions import InvalidClientException


class ClientFactory:
    """Factory for creating all clients with the same API key."""

    def __init__(self, api_key: str) -> None:
        """Init Factory with the API key to use when creating clients.

        Args:
            api_key: The API key to use when instantiating all clients
        """
        self.api_key = api_key

    def build(self, client_name: str) -> Client:
        """Import and instantiate the required class.

        Args:
            client_name: The name of the client to create. Should match the
                name of the module, minus the "_client" part.

        Returns:
            An instance of the client, creates with the API key held on the class.

        Raises:
            InvalidClientException: Rasied when the client module or
                class cannot be found
        """
        module_name = f".{client_name}_client"
        client_class_name = f"{client_name.title()}Client"

        try:
            client_module = import_module(f"{module_name}", "pybomb.clients")

            return getattr(client_module, client_class_name)(self.api_key)
        except (ModuleNotFoundError, AttributeError) as e:
            raise InvalidClientException from e
