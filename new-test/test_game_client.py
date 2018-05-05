import pytest
from mock import patch, MagicMock
from requests.models import Response as RequestsResponse
from requests.exceptions import HTTPError


from pybomb.clients.game_client import GameClient
from pybomb.exceptions import InvalidReturnFieldException, BadRequestException
from pybomb.response import Response


class TestGameClient:
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
            'results': {'id': 1, 'description': 'Great Game'},
        }

        return mock_response

    @pytest.fixture
    def game_client(self, mock_response, mock_requests_get):
        mock_requests_get.return_value = mock_response
        game_client = GameClient('fake_key')

        return game_client

    def test_can_fetch_game(self, game_client, mock_response, mock_requests_get):
        res = game_client.fetch(1)

        assert isinstance(res, Response)
        assert res.uri == mock_response.url

        mock_response_json = mock_response.json()
        assert res.num_page_results == (
            mock_response_json['number_of_page_results']
        )
        assert res.num_total_results == (
            mock_response_json['number_of_total_results']
        )

        # TODO - use the version number param
        mock_requests_get.assert_called_once_with(
            'http://www.giantbomb.com/api/game/1',
            params={'api_key': 'fake_key', 'format': 'json'},
            headers={'User-Agent': 'Pybomb 0.1.6'}
        )

    def test_can_specify_return_fields(self, game_client, mock_requests_get):
        res = game_client.fetch(1, ('id', 'name'))
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

    def test_invalid_response(self, game_client, mock_response):
        mock_response.raise_for_status.side_effect = HTTPError('Test error')

        with pytest.raises(BadRequestException):
            res = game_client.fetch(1)
