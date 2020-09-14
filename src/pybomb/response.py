"""The response types and factories for PyBomb."""
from typing import NamedTuple, Optional

from requests import Response as RequestsResponse


class Response(NamedTuple):
    """An API response."""

    uri: str
    num_page_results: int
    num_total_results: int
    results: list
    result: Optional[dict]

    @classmethod
    def from_response_data(cls, response_data: RequestsResponse) -> "Response":
        """Response factory.

        If the response is from a fetch client and "results" is not wrapped in
        a list, the single result will be stored in results in a list and the
        original result will be added to result.

        If the response is from a search client and "results" is a list, this list
        will be stored in results and result will be empty.

        Either way, results will always hold the results in list format.

        Args:
            response_data: Raw request response of API call

        Returns:
            A PyBomb Response containing the raw response data.
        """
        response_json = response_data.json()

        cls_args = [
            response_data.url,
            response_json["number_of_page_results"],
            response_json["number_of_total_results"],
        ]

        if isinstance(response_json["results"], dict):
            cls_args.extend(([response_json["results"]], response_json["results"]))
        else:
            cls_args.extend((response_json["results"], None))

        return cls(*cls_args)
