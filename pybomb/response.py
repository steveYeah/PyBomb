"""
The response types and factories for PyBomb
"""
from collections import namedtuple


class Response(
    namedtuple(
        'Response', ('uri', 'num_page_results', 'num_total_results', 'results')
    )
):
    """
    An API response
    """

    @classmethod
    def from_response_data(cls, response_data):
        """
        Response factory

        :param response_data: requests.models.Response
        :return: pybomb.clients.Response
        """

        response_json = response_data.json()

        return cls(
            response_data.url,
            response_json['number_of_page_results'],
            response_json['number_of_total_results'],
            response_json['results']
        )
