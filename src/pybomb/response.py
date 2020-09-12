"""The response types and factories for PyBomb."""
from typing import NamedTuple, Union

from requests import Response as RequestsResponse


class Response(NamedTuple):
    """An API response."""

    uri: str
    num_page_results: int
    num_total_results: int
    results: Union[list, dict]

    @classmethod
    def from_response_data(cls, response_data: RequestsResponse) -> "Response":
        """Response factory.

        Args:
            response_data: Raw request response of API call

        Returns:
            A PyBomb Response containing the raw response data
        """
        response_json = response_data.json()

        return cls(
            response_data.url,
            response_json["number_of_page_results"],
            response_json["number_of_total_results"],
            response_json["results"],
        )
