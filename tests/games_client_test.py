from nose.tools import *
from nose.plugins.attrib import attr
import pybomb
from pybomb.response import Response
from pybomb.clients.games_client import GamesClient


def setup():
    global games_client, return_fields, sort_by, filter_by, limit, offset

    class MockResponse(object):
        def __init__(self):
            self.url = ''
            self.num_total_results = 1
            self.num_page_results = 1
            self.results = ['result']
            self.status_code = GamesClient.RESPONSE_STATUS_OK

        def json(self):
            return {
                'number_of_total_results': self.num_total_results,
                'number_of_page_results': self.num_page_results,
                'results': self.results,
                'status_code': self.status_code,
            }

        def raise_for_status(self):
            return None

    def _query_api(params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        return MockResponse()

    games_client = GamesClient('mock_api_key')
    games_client._query_api = _query_api

    return_fields = (
        'api_detail_url',
        'date_added',
        'date_last_updated',
        'deck',
        'description',
        'expected_release_month',
        'expected_release_quarter',
        'expected_release_year',
        'id',
        'image',
        'name',
        'number_of_user_reviews',
        'original_game_rating',
        'original_release_date',
        'platforms',
        'site_detail_url'
    )

    sort_by = 'date_added'

    filter_by = {
        'aliases': None,
        'date_added': None,
        'date_last_updated': None,
        'expected_release_month': None,
        'expected_release_quarter': None,
        'expected_release_year': None,
        'id': None,
        'name': None,
        'number_of_user_reviews': None,
        'original_release_date': None,
        'platforms': None
    }

    limit = 10
    offset = 100


def test_full_search_should_return_response():
    """
    When the search function is used correctly then it should return a response
    """
    response = games_client.search(filter_by, return_fields, sort_by, False, limit, offset)
    assert isinstance(response, Response)


@raises(pybomb.exceptions.InvalidFilterFieldException)
def test_full_search_filter_by_field():
    """
    pybomb.exceptions.InvalidFilterFieldException is thrown when trying to use an invalid filter
    field
    """
    invalid_filter_by = {'Bob': False}
    games_client.search(invalid_filter_by, return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidFilterFieldException)
def test_full_search_filter_by_field_not_a_valid_filter():
    """
    pybomb.exceptions.InvalidFilterFieldException is thrown when trying to use a valid field
    that cannot be used as a filter
    """
    invalid_filter_by = {'api_detail_url': False}
    games_client.search(invalid_filter_by, return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidReturnFieldException)
def test_full_search_invalid_return_field():
    """
    pybomb.exceptions.InvalidReturnFieldException is thrown when trying to use an invalid return
    field
    """
    invalid_return_fields = {'Bob': False}
    games_client.search(filter_by, invalid_return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidSortFieldException)
def test_full_search_invalid_sort_by_field():
    """
    pybomb.exceptions.InvalidSortFieldException is thrown when trying to use an invalid sort field
    """
    invalid_sort_by = 'Bob'
    games_client.search(filter_by, return_fields, invalid_sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidSortFieldException)
def test_full_search_invalid_sort_by_field_not_a_valid_sort():
    """
    pybomb.exceptions.InvalidSortFieldException is thrown when trying to use a valid field that cannot be used for sorting
    """
    invalid_sort_by = 'aliases'
    games_client.search(filter_by, return_fields, invalid_sort_by, True, limit, offset)



@raises(ValueError)
def test_invalid_limit():
    """
    ValueError is thrown when trying to use a data type that cannot be cast to an int as the limit
    field
    """
    games_client.search(filter_by, return_fields, sort_by, True, 'bob', offset)


@raises(ValueError)
def test_invalid_offset():
    """
    ValueError is thrown when trying to use a data type that cannot be cast to an int as the offset
    field
    """
    games_client.search(filter_by, return_fields, sort_by, True, limit, 'bob')


def test_quick_search_should_return_response():
    """
    When the quick search function is used correctly then it should return a response
    """
    response = games_client.quick_search('deus ex', pybomb.PS3)
    assert isinstance(response, Response)


@attr('web')
@raises(pybomb.exceptions.BadRequestException)
def test_search_bad_request():
    bad_request_client = GamesClient('mock key')
    bad_request_client.URI_BASE = 'http://httpbin.org/status/404'

    bad_request_client.search(filter_by, return_fields, sort_by, False, limit, offset)


@attr('web')
@raises(pybomb.exceptions.BadRequestException)
def test_quick_search_bad_request():
    bad_request_client = GamesClient('mock key')
    bad_request_client.URI_BASE = 'http://httpbin.org/status/404'

    bad_request_client.quick_search('deus ex', pybomb.PS3)


@raises(pybomb.exceptions.InvalidResponseException)
def test_search_bad_response():
    class MockBadResponse(object):
        def __init__(self):
            self.url = ''
            self.num_total_results = 1
            self.num_page_results = 1
            self.results = ['result']
            self.status_code = 100

        def json(self):
            return {
                'number_of_total_results': self.num_total_results,
                'number_of_page_results': self.num_page_results,
                'results': self.results,
                'status_code': self.status_code,
                'error': 'Invalid API Key'
            }

        def raise_for_status(self):
            return None

    def _query_api(params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        return MockBadResponse()

    bad_response_client = GamesClient('mock key')
    bad_response_client._query_api = _query_api

    bad_response_client.search(filter_by, return_fields, sort_by, False, limit, offset)


@raises(pybomb.exceptions.InvalidResponseException)
def test_quick_search_bad_response():
    class MockBadResponse(object):
        def __init__(self):
            self.url = ''
            self.num_total_results = 1
            self.num_page_results = 1
            self.results = ['result']
            self.status_code = 100

        def json(self):
            return {
                'number_of_total_results': self.num_total_results,
                'number_of_page_results': self.num_page_results,
                'results': self.results,
                'status_code': self.status_code,
                'error': 'Invalid API Key'
            }

        def raise_for_status(self):
            return None

    def _query_api(params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        return MockBadResponse()

    bad_response_client = GamesClient('mock key')
    bad_response_client._query_api = _query_api

    bad_response_client.quick_search('deus ex', pybomb.PS3)
