"""
The response types and factories for PyBomb
"""


def create_response(response):
    """
    Response factory

    :param response: requests.models.Response
    :return: pybomb.clients.Response
    """

    response_json = response.json()

    return Response(
        response.url,
        response_json['number_of_total_results'],
        response_json['results']
    )


class Response(object):
    """
    An API response
    """

    def __init__(self, uri, num_results, results):
        """
        :param uri: string
        :param num_results: int
        :param results: list
        """
        self.__uri = uri
        self.__num_results = num_results
        self.__results = results

    @property
    def uri(self):
        """
        Origin of response

        :return: string
        """
        return self.__uri

    @property
    def num_results(self):
        """
        Number of results

        :return: int
        """
        return self.__num_results

    @property
    def results(self):
        """
        List of core results

        :return: list
        """
        return self.__results
