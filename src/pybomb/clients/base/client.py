"""Base client used by fetch and search clients."""
from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple, Union

import pkg_resources
from requests import Response as RequestsResponse
from requests.exceptions import HTTPError

from pybomb.exceptions import (
    BadRequestException,
    InvalidFilterFieldException,
    InvalidResponseException,
    InvalidReturnFieldException,
    InvalidSortFieldException,
)
from pybomb.response import Response


class ResponseParam(NamedTuple):
    """Control structure for marking fields as filter-able and sort-able."""

    is_filter: bool
    is_sort: bool


class Client(ABC):
    """Base class for GB API resource clients."""

    URI_BASE = "http://www.giantbomb.com/api/"

    RESPONSE_FIELD_MAP: Dict[str, ResponseParam] = {}
    RESPONSE_STATUS_OK = 1
    RESPONSE_FORMAT_JSON = "json"

    RESOURCE_NAME = ""

    SORT_ORDER_ASCENDING = "asc"
    SORT_ORDER_DESCENDING = "desc"

    def __init__(self, api_key: str) -> None:
        """Init Client with GB API key and default_response_format.

        Args:
            api_key: The GB API key to use for each request
        """
        self.api_key = api_key
        self._headers = {
            "User-Agent": f'Pybomb {pkg_resources.require("pybomb")[0].version}'
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
                    f'"{return_field}" is an invalid return field'
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
            raise InvalidSortFieldException(f'"{sort_by}" is an invalid sort field')

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
                    f'"{filter_field}" is an invalid filter field'
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
            [f"{key}:{value}" for key, value in filter_by.items() if value is not None]
        )

    def _query(self, params: Dict[str, Union[str, int]]) -> Response:
        """Add required params, call GB API and format the response.

        Args:
            params: All of the params requested for the call

        Returns:
            A Response object containing the GB API response
        """
        params["api_key"] = self.api_key
        params["format"] = self.RESPONSE_FORMAT_JSON

        response = self._query_api(params)
        self._validate_response(response)

        return Response.from_response_data(response)

    @abstractmethod
    def _query_api(self, params: Dict[str, Union[str, int]]) -> RequestsResponse:
        """Handle actual query to GB API.

        Args:
            params: All requests and required resource query parameters

        Returns:
            The raw requests Response from the GB call
        """
        return RequestsResponse()  # pragma: no cover

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
                f'Response code {response_data["status_code"]}: {response_data["error"]}'
            )
