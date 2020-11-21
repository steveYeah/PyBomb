"""Base client to extend to create fetch clients for endpoints of the GiantBomb API."""
from typing import Dict, Union

from requests import get, Response as RequestsResponse

from pybomb.clients.base.client import Client


class FetchClient(Client):
    """Base class for fetch GB API resource clients."""

    def _query_api(self, params: Dict[str, Union[str, int]]) -> RequestsResponse:
        """Handle actual query to GB API.

        Args:
            params: All requests and required resource query parameters

        Returns:
            The raw requests Response from the GB call
        """
        id = params.pop("id")
        return get(
            f"{self.URI_BASE}{self.RESOURCE_NAME}/{id}",
            params=params,
            headers=self._headers,
        )
