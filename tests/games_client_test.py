from nose.tools import *
import pybomb
from pybomb.response import Response
from pybomb.clients.games_client import GamesClient


def setup():
    global games_client, return_fields, sort_by, filter_by, limit, offset

    class MockResponse(object):
        def __init__(self):
            self.url = ''
            self.num_results = 1
            self.results = ['result']

        def json(self):
            return {
                'number_of_total_results': self.num_results,
                'results': self.results,
                'status_code': pybomb.GamesClient.RESPONSE_STATUS_OK
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
    response = games_client.search(filter_by, return_fields, sort_by, False, limit, offset)
    assert isinstance(response, Response)


@raises(pybomb.exceptions.InvalidFilterFieldException)
def test_full_search_filter_by_field():
    invalid_filter_by = {'Bob': False}
    games_client.search(invalid_filter_by, return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidFilterFieldException)
def test_full_search_filter_by_field_not_a_valid_filter():
    invalid_filter_by = {'api_detail_url': False}
    games_client.search(invalid_filter_by, return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidReturnFieldException)
def test_full_search_invalid_return_field():
    invalid_return_fields = {'Bob': False}
    games_client.search(filter_by, invalid_return_fields, sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidSortFieldException)
def test_full_search_invalid_sort_by_field():
    invalid_sort_by = 'Bob'
    games_client.search(filter_by, return_fields, invalid_sort_by, True, limit, offset)


@raises(pybomb.exceptions.InvalidSortFieldException)
def test_full_search_invalid_sort_by_field_not_a_valid_sort():
    invalid_sort_by = 'aliases'
    games_client.search(filter_by, return_fields, invalid_sort_by, True, limit, offset)


@raises(ValueError)
def test_invalid_limit():
    games_client.search(filter_by, return_fields, sort_by, True, 'bob', offset)


@raises(ValueError)
def test_invalid_offset():
    games_client.search(filter_by, return_fields, sort_by, True, limit, 'bob')


def test_quick_search_should_return_response():
    response = games_client.quick_search('deus ex', pybomb.PS3)
    assert isinstance(response, Response)


# test actual request exceptions that can be tested