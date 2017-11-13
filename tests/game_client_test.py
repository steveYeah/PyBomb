from mock import Mock
from nose.tools import *
from nose.plugins.attrib import attr

import pybomb
from pybomb.response import Response
from pybomb.clients.game_client import GameClient


def setup():
    global game_client, bad_response_client, bad_request_client
    global return_fields

    mock_response = Mock()
    mock_response.json.return_value = {
        'status_code': GameClient.RESPONSE_STATUS_OK,
        'number_of_page_results': 1,
        'number_of_total_results': 1,
        'results': {},
    }
    mock_response.raise_for_status.return_value = None

    game_client = GameClient('mock_api_key')
    game_client._query_api = Mock(return_value=mock_response)

    bad_request_client = GameClient('mock_api_key')
    bad_request_client.URI_BASE = 'http://httpbin.org/status/404'

    mock_bad_response = Mock()
    mock_bad_response.json.return_value = {
        'status_code': 100,
        'error': 'Invalid API Key',
    }
    mock_bad_response.raise_for_status.return_value = None

    bad_response_client = GameClient('mock_api_key')
    bad_response_client._query_api = Mock(return_value=mock_bad_response)


def test_fetch_returns_response():
    response = game_client.fetch(1)

    assert isinstance(response, Response)


@raises(pybomb.exceptions.InvalidReturnFieldException)
def test_fetch_invalid_return_field():
    invalid_return_field = {'Bob': False}
    game_client.fetch(1, invalid_return_field)


@attr('web')
@raises(pybomb.exceptions.BadRequestException)
def test_fetch_bad_request():
    bad_request_client.fetch(1)


@raises(pybomb.exceptions.InvalidResponseException)
def test_fetch_bad_response():
    bad_response_client.fetch(1)
