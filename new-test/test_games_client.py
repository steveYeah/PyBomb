import pkg_resources

import pytest
from mock import patch, MagicMock
from requests.models import Response as RequestsResponse
from requests.exceptions import HTTPError


from pybomb.clients.games_client import GamesClient
from pybomb.exceptions import (
    InvalidReturnFieldException,
    BadRequestException,
    InvalidResponseException,
    InvalidSortFieldException,
)
from pybomb.response import Response


version = pkg_resources.require("pybomb")[0].version


class TestGamesClient:
    @pytest.fixture
    def mock_requests_get(self):
        with patch('pybomb.clients.base_client.get') as req_mock:
            yield req_mock

    @pytest.fixture
    def mock_response(self):
        mock_response = MagicMock(RequestsResponse)
        mock_response.url = 'https://fake.com'

        mock_response.json.return_value = {
            'status_code': 1,
            'number_of_page_results': 1,
            'number_of_total_results': 1,
            'results': [{'id': 1, 'description': 'Great Game'}],
        }

        return mock_response

    @pytest.fixture
    def games_client(self, mock_response, mock_requests_get):
        mock_requests_get.return_value = mock_response
        games_client = GamesClient('fake_key')

        return games_client

    class TestQuickSearch:
        def test_search(self, games_client, mock_response, mock_requests_get):
            res = games_client.quick_search('game name')

            assert isinstance(res, Response)
            assert res.uri == mock_response.url

            mock_response_json = mock_response.json()
            assert res.results == mock_response_json['results']

            assert res.num_page_results == (
                mock_response_json['number_of_page_results']
            )

            assert res.num_total_results == (
                mock_response_json['number_of_total_results']
            )

            mock_requests_get.assert_called_once_with(
                'http://www.giantbomb.com/api/games',
                params={
                    'filter': 'name:game name',
                    'api_key': 'fake_key',
                    'format': 'json'
                },
                headers={'User-Agent': 'Pybomb {}'.format(version)}
            )

        @pytest.mark.parametrize(
            'sort_dec, sort_direction', [(True, 'desc'), (False, 'asc')]
        )
        def test_sort(
            self, sort_dec, sort_direction, games_client, mock_response,
            mock_requests_get
        ):
            res = games_client.quick_search(
                'game name', sort_by='date_added', desc=sort_dec
            )
            assert isinstance(res, Response)

            mock_requests_get.assert_called_once_with(
                'http://www.giantbomb.com/api/games',
                params={
                    'filter': 'name:game name',
                    'sort': (f'date_added:{sort_direction}',),
                    'api_key': 'fake_key',
                    'format': 'json'
                },
                headers={'User-Agent': 'Pybomb {}'.format(version)}
            )

        def test_invaild_sort(self, games_client):
            with pytest.raises(InvalidSortFieldException):
                res = games_client.quick_search('game name', sort_by='aliases')

        def test_bad_giantbomb_request(self, games_client, mock_response):
            mock_response.raise_for_status.side_effect = HTTPError('Test error')

            with pytest.raises(BadRequestException):
                res = games_client.quick_search('bad search')

        def test_bad_giantbomb_response(self, games_client, mock_response):
            mock_response_json = mock_response.json()
            mock_response_json['status_code'] = 2
            mock_response_json['error'] = 'Badness'
            mock_response.json.return_value = mock_response_json

            with pytest.raises(InvalidResponseException):
                res = games_client.quick_search('bad search')

    class TestSearch:
        def test_filter_search(self):
            assert False

        def test_invalid_filters(self):
            assert False

        def test_can_specify_return_fields(
            self, games_client, mock_requests_get
        ):
            res = games_client.fetch(1, ('id', 'name'))
            assert isinstance(res, Response)

            # TODO - use the version number param
            mock_requests_get.assert_called_once_with(
                'http://www.giantbomb.com/api/game/1',
                params={
                    'field_list': 'id,name',
                    'api_key': 'fake_key',
                    'format': 'json'
                },
                headers={'User-Agent': 'Pybomb 0.1.6'}
        )

        def test_invalid_return_fields(self, game_client, mock_response):
            with pytest.raises(InvalidReturnFieldException):
                res = game_client.fetch(1, ('bad', 'params'))

        def test_sort(self):
            assert False

        def test_invaild_sort(self):
            assert False

        def test_desc(self):
            assert False

        def test_limit(self):
            assert False

        def test_offset(self):
            assert False
