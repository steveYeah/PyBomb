"""Base client to extend to create clients for endpoints of the GiantBomb API."""
from collections import namedtuple
from typing import Dict, List, Union

import pkg_resources
from requests import get, Response as RequestsResponse
from requests.exceptions import HTTPError


from pybomb.exceptions import (
    BadRequestException,
    InvalidFilterFieldException,
    InvalidResponseException,
    InvalidReturnFieldException,
    InvalidSortFieldException,
)
from pybomb.response import Response


ResponseParam = namedtuple("ResponseParam", ("is_filter", "is_sort"))


class BaseClient(object):
    """Base class for GB API resource clients."""

    URI_BASE = "http://www.giantbomb.com/api/"
    RESPONSE_FORMAT_JSON = "json"
    RESPONSE_FORMAT_XML = "xml"
    RESPONSE_FIELD_MAP: Dict[str, ResponseParam] = {}
    RESPONSE_STATUS_OK = 1

    RESOURCE_NAME = ""

    SORT_ORDER_ASCENDING = "asc"
    SORT_ORDER_DESCENDING = "desc"

    def __init__(
        self, api_key: str, default_format: str = RESPONSE_FORMAT_JSON
    ) -> None:
        """Init BaseClient with GB API key and default_response_format.

        Args:
            api_key: The GB API key to use for each request
            default_format: The default response format for the return data.
                TODO: Why?
        """
        self.api_key = api_key
        self.default_format = default_format
        self._headers = {
            "User-Agent": "Pybomb {0}".format(
                pkg_resources.require("pybomb")[0].version
            )
        }

    def _validate_return_fields(self, return_fields: List[str]) -> None:
        """Validate the given return fields against those allowed on the resource.

        Args:
            return_fields: Requested return fields

        Raises:
            InvalidReturnFieldException: Invalid return fields
                requested for the resource.
        """
        for return_field in return_fields:
            if return_field not in self.RESPONSE_FIELD_MAP:
                raise InvalidReturnFieldException(
                    '"{0}" is an invalid return field'.format(return_field)
                )

    def _validate_sort_field(self, sort_by: str) -> None:
        """Validate the given sort field against those allowed on the resource.

        Args:
            sort_by: The field to sort the response by

        Raises:
            InvalidSortFieldException: Invalid sort supplied for the resource
        """
        if (
            sort_by not in self.RESPONSE_FIELD_MAP
            or not self.RESPONSE_FIELD_MAP[sort_by].is_sort
        ):
            raise InvalidSortFieldException(
                '"{0}" is an invalid sort field'.format(sort_by)
            )

    def _validate_filter_fields(self, filter_by: Dict[str, Union[str, int]]) -> None:
        """Validate the given filter fields against those allowed on the resource.

        Args:
            filter_by: Requested filter fields

        Raises:
            InvalidFilterFieldException: Invalid filter fields requested
                for the resource
        """
        for filter_field in filter_by:
            if (
                filter_field not in self.RESPONSE_FIELD_MAP
                or not self.RESPONSE_FIELD_MAP[filter_field].is_filter
            ):
                raise InvalidFilterFieldException(
                    '"{0}" is an invalid filter field'.format(filter_field)
                )

    @staticmethod
    def _create_search_filter(filter_by: Dict[str, Union[str, int]]) -> str:
        """Create a filter string to be used for the request using the supplied filters.

        Args:
            filter_by: Requested filter fields

        Returns:
            A string containing the filters in the format required by GB API
        """
        return ",".join(
            [
                "{0}:{1}".format(key, value)
                for key, value in filter_by.items()
                if value is not None
            ]
        )

    def _query(
        self, params: Dict[str, Union[str, int]], direct: bool = False
    ) -> Response:
        """Add required params, call GB API and format the response.

        Args:
            params: All of the params requested for the call
            direct: Is this a direct call for a resource or a search query

        Returns:
            A Response object containing the GB API response
        """
        params["api_key"] = self.api_key
        params["format"] = self.default_format

        response = self._query_api(params, direct)
        self._validate_response(response)

        return Response.from_response_data(response)

    def _query_api(
        self, params: Dict[str, Union[str, int]], direct: bool = False
    ) -> RequestsResponse:
        """Handle actual query to GB API.

        Args:
            params: All requests and required resource query parameters
            direct: Is this a direct call for a resource or a search query

        Returns:
            The raw requests Response from the GB call
        """
        if not direct:
            return get(
                self.URI_BASE + self.RESOURCE_NAME, params=params, headers=self._headers
            )

        id = params.pop("id")
        return get(
            self.URI_BASE + self.RESOURCE_NAME + "/{0}".format(id),
            params=params,
            headers=self._headers,
        )

    def _validate_response(self, response: RequestsResponse) -> None:
        """Validate the response from the GB API.

        Args:
            response: The raw requests response from the GB call

        Raises:
            InvalidResponseException: The response was invalid
            BadRequestException: The request to the GB API was invalid
        """
        try:
            response.raise_for_status()
        except HTTPError as http_error:
            raise BadRequestException(str(http_error))

        response_data = response.json()
        if response_data["status_code"] != self.RESPONSE_STATUS_OK:
            raise InvalidResponseException(
                "Response code {0}: {1}".format(
                    response_data["status_code"], response_data["error"]
                )
            )
