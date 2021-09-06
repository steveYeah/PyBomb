"""Base client to extend to create search clients for endpoints of the GiantBomb API."""
from abc import abstractmethod
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
             A PyBomb Response containing the results of the search
        """
        self._validate_filter_fields(filter_by)
        search_filter = self._create_search_filter(filter_by)

        search_params: Dict[str, Union[str, int]] = {"filter": search_filter}
        self._apply_return_fields(return_fields, search_params)
        self._apply_sort_by(sort_by, desc, search_params)
        self._apply_limit(limit, search_params)
        self._apply_offset(offset, search_params)

        response = self._query(search_params)

        return response

    @abstractmethod
    def quick_search(
        self,
        name: str,
        sort_by: Optional[str] = None,
        desc: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Search with a simplier API."""
        ...  # pragma: no cover

    def _apply_return_fields(
        self, return_fields: Optional[List], search_params: Dict[str, Union[str, int]],
    ) -> None:
        """Apply return filters to search params if any were supplied.

        Args:
            return_fields: A list of fields to be returned by the response.
                These will be validated against the availiable return fields.
                The default is to return everything
            search_params: A dictionary containing all search params
        """
        if return_fields is None:
            return

        self._validate_return_fields(return_fields)
        field_list = ",".join(return_fields)

        search_params["field_list"] = field_list

    def _apply_sort_by(
        self,
        sort_by: Optional[str],
        desc: bool,
        search_params: Dict[str, Union[str, int]],
    ) -> None:
        """Apply sort by to search params if one was supplied.

        Args:
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True
            search_params: A dictionary containing all search params
        """
        if sort_by is None:
            return

        self._validate_sort_field(sort_by)

        if desc:
            direction = self.SORT_ORDER_DESCENDING
        else:
            direction = self.SORT_ORDER_ASCENDING

        search_params["sort"] = f"{sort_by}:{direction}"

    def _apply_limit(
        self, limit: Optional[int], search_params: Dict[str, Union[str, int]],
    ) -> None:
        """Apply the limit to the search params if one was supplied.

        Args:
            limit: The max number of items to request
            search_params: A dictionary containing all search params

        """
        if limit is None:
            return

        search_params["limit"] = int(limit)

    def _apply_offset(
        self, offset: Optional[int], search_params: Dict[str, Union[str, int]],
    ) -> None:
        """Add the offset to search params if one was supplied.

        Args:
            offset: The start offset for the return items, based on the given sort.
            search_params: A dictionary containing all search params
        """
        if offset is None:
            return

        search_params["offset"] = int(offset)

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
