"""Base client to extend to create search clients for endpoints of the GiantBomb API."""
from typing import Any, Dict, List, Optional, Union

from requests import get, Response as RequestsResponse

from pybomb.clients.base.client import Client
from pybomb.response import Response


class SearchClient(Client):
    """Base class for search GB API resource clients."""

    def search(
        self,
        filter_by: Dict[str, Any],
        return_fields: List = None,
        sort_by: Optional[str] = None,
        desc: bool = True,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Response:
        """Full search of resource.

        Supports all search fields available in API
        http://www.giantbomb.com/api/documentation

        Args:
            filter_by: A map of fields to filter the search by. These will
                be validated against the availiable search fields
            return_fields: A list of fields to be returned by the response.
                These will be validated against the availiable return fields.
                The default is to return everything
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True
            limit: The max number of items to request
            offset: The start offset for the return items, based on the given sort.

        Returns:
             A PyBomb Response containg the results of the search
        """
        self._validate_filter_fields(filter_by)
        search_filter = self._create_search_filter(filter_by)

        search_params: Dict[str, Union[str, int]] = {"filter": search_filter}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ",".join(return_fields)

            search_params["field_list"] = field_list

        if sort_by is not None:
            self._validate_sort_field(sort_by)

            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params["sort"] = f"{sort_by}:{direction}"

        if limit is not None:
            search_params["limit"] = int(limit)

        if offset is not None:
            search_params["offset"] = int(offset)

        response = self._query(search_params)

        return response

    def _quick_search(
        self, query_filter: str, desc: bool, sort_by: Optional[str] = None
    ) -> Response:
        """Search with a simplier API.

        This method allows you to search for a game using only the title and
        the platform.

        Args:
            query_filter: The filters to use for the search
            desc: If sort direction is DESC or not (ASC). Defaults to True
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.

        Returns:
             A PyBomb Response containg the results of the search
        """
        search_params: Dict[str, Union[str, int]] = {"filter": query_filter}

        if sort_by is not None:
            self._validate_sort_field(sort_by)

            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params["sort"] = f"{sort_by}:{direction}"

        response = self._query(search_params)

        return response

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
