"""Base client to extend to create search clients for endpoints of the GiantBomb API."""
from typing import Dict, Union

from requests import get, Response as RequestsResponse

from pybomb.clients.base.client import Client


class SearchClient(Client):
    """Base class for search GB API resource clients."""

    def _query_api(self, params: Dict[str, Union[str, int]]) -> RequestsResponse:
        """Handle actual query to GB API.

        Args:
            params: All requests and required resource query parameters

        Returns:
            The raw requests Response from the GB call
        """
        return get(
            self.URI_BASE + self.RESOURCE_NAME, params=params, headers=self._headers
        )
