"""The response types and factories for PyBomb."""
from collections import namedtuple

from requests import Response as RequestsResponse


class Response(
    namedtuple("Response", ("uri", "num_page_results", "num_total_results", "results"))
):
    """An API response."""

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
