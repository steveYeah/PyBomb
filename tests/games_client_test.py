import pytest
from mock import Mock, patch

from pybomb.clients.games_client import GamesClient


@pytest.fixture
def games_client():
    games_client = GamesClient('mock_api_key')

    return games_client

# need to mock out requests.get
# response.json()
# response_json = response_data.json()
#   return cls(
#       response_data.url,
#       response_json['number_of_page_results'],
#       response_json['number_of_total_results'],
#       response_json['results']
#   )


@pytest.fixture
@patch('pybomb.clients.base_client.requests')
def fake_request(mock_requests):
    mock_json_data = {
        'number_of_page_results': 1,
        'number_of_total_results': 1,
        'results': []
    }

    get_mock = Mock()
    get_mock.json.return_value = mock_json_data
    mock_requests.get.return_value = get_mock

    return mock_requests


class TestFullSearch:

    def test_return_valid_response(self, fake_request, games_client):
        games_client.search(
            filter_by=filter_by,
            return_fields=return_fields,
            sort_by=sort_by,
            desc=True,
            limit=limit,
            offset=offset
        )
        assert False

    def test_unknown_filter():
        assert False

    def test_invalid_filter():
        assert False

    def test_unknown_sort():
        assert False

    def test_invalid_sort():
        assert False

    def test_invalid_return_field():
        assert False

    def test_invalid_limit():
        assert False

    def test_invalid_offset():
        assert False

    def test_search_bad_request():
        assert False

    def test_search_bad_response():
        assert False


class TestQuickSearch:

    def test_quick_search_should_return_response():
        assert False

    def test_quick_search_bad_request():
        assert False

    def test_quick_search_bad_response():
        assert False
