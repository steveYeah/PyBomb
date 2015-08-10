# @todo restructure
# @todo add tests
# @todo pep8
# @todo pylint
# @todo add platform IDs


import requests


class ClientException(Exception):
    """
    Base Exception for module
    """
    pass


class InvalidReturnFieldException(ClientException):
    """
    Exception for invalid return fields
    """
    pass


class InvalidSortFieldException(ClientException):
    """
    Exception for invalid sort fields
    """
    pass


class InvalidFilterFieldException(ClientException):
    """
    Exception for invalid filter fields
    """
    pass


class InvalidResponseException(ClientException):
    """
    Exception thrown when receiving an invalid response from selected resource
    """
    pass


# @todo implement
class Response(object):
    """
    Represents a response from all resources
    """
    pass


class BaseClient(object):
    """
    Base class for API resource clients
    """

    URI_BASE = 'http://www.giantbomb.com/api/'
    RESPONSE_FORMAT_JSON = 'json'
    RESPONSE_FORMAT_XML = 'xml'

    SORT_BY_FIELD = 0
    SORT_BY_DIRECTION = 1

    RESPONSE_STATUS_OK = 1

    def __init__(self, api_key, default_format=RESPONSE_FORMAT_JSON):
        """
        :param api_key: string
        :param default_format: string
        """
        self._api_key = api_key
        self._default_format = default_format

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    @property
    def default_format(self):
        return self._default_format

    def _validate_return_fields(self, return_fields):
        """
        :param return_fields: tuple
        :raises: InvalidReturnFieldException
        """
        for return_field in return_fields:
            if return_field not in self.RESPONSE_FIELD_MAP:
                raise InvalidReturnFieldException(
                    '"{}" is an invalid return field'.format(return_field)
                )

    def _validate_sort_field(self, sort_by):
        """
        :param sort_by: tuple
        :raises: InvalidSortFieldException
        """
        if (
            sort_by[self.SORT_BY_FIELD] not in self.RESPONSE_FIELD_MAP or
            not self.RESPONSE_FIELD_MAP[sort_by[self.SORT_BY_FIELD]][self.SORT_FIELD]
        ):
            raise InvalidSortFieldException(
                '"{}" is an invalid sort field'.format(sort_by[self.SORT_BY_FIELD])
            )

    def _validate_filter_fields(self, filter_by):
        """
        :param filter_by: dict
        :raises: InvalidFilterFieldException
        """
        for filter_field in filter_by:
            if (
                filter_field not in self.RESPONSE_FIELD_MAP or
                not self.RESPONSE_FIELD_MAP[filter_field][self.FILTER_FIELD]
            ):
                raise InvalidFilterFieldException(
                    '"{}" is an invalid filter field'.format(filter_field)
                )

    def _create_search_filter(self, filter_by):
        """
        :param filter_by:
        :return: dict
        """
        return ','.join(
            ['{}:{}'.format(key, value) for key, value in filter_by.iteritems()]
        )

    def _query(self, params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        params['api_key'] = self._api_key

        if 'format' not in params:
            params['format'] = self._default_format

        response = requests.get(self.URI_BASE + self.RESOURCE_NAME, params)
        self._validate_response(response)

        # @todo map to response object
        return response

    def _validate_response(self, response):
        """
        :param response: requests.models.Response
        :raises: InvalidResponseException
        """

        # @todo catch and raise InvalidResponseException
        response.raise_for_status()
        response_data = response.json()

        if response_data['status_code'] != self.RESPONSE_STATUS_OK:
            raise InvalidResponseException('Response code {}: {}'.format(
                response_data['status_code'],
                response_data['error'])
            )


class GamesClient(BaseClient):
    """
    Client for the 'games' API resource
    """

    RESOURCE_NAME = 'games'

    FILTER_FIELD = 0
    SORT_FIELD = 1

    RESPONSE_FIELD_MAP = {
        'aliases': (True, False),
        'api_detail_url': (False, False),
        'date_added': (True, True),
        'date_last_updated': (True, True),
        'deck': (False, False),
        'description': (False, False),
        'expected_release_month': (True, False),
        'expected_release_quarter': (True, False),
        'expected_release_year': (True, False),
        'id': (True, True),
        'image': (False, False),
        'name': (True, True),
        'number_of_user_reviews': (True, True),
        'original_game_rating': (False, True),
        'original_release_date': (True, True),
        'platforms': (True, False),
        'site_detail_url': (False, False),
    }

    def search(self, return_fields, limit, offset, sort_by, filter_by):
        """
        Full search of games resource, supporting all search fields available in API
        http://www.giantbomb.com/api/documentation#toc-0-15

        :param return_fields: tuple
        :param limit: int
        :param offset: int
        :param sort_by: tuple
        :param filter_by: dict
        :return: requests.models.Response
        """
        self._validate_sort_field(sort_by)
        self._validate_return_fields(return_fields)
        self._validate_filter_fields(filter_by)

        search_filter = self._create_search_filter(filter_by)
        field_list = ','.join(return_fields)

        search_params = {
            'filter': search_filter,
            'field_list': field_list,
            'sort': '{}:{}'.format(sort_by[self.SORT_BY_FIELD], sort_by[self.SORT_BY_DIRECTION]),
            'limit': int(limit),
            'offset': int(offset)
        }

        response = self._query(search_params)

        return response

    def quick_search(self, name, platform=None):
        """
        Quick search method that allows you to search for a game using only the
        title and the platform

        :param name: string
        :param platform: int
        :return: requests.models.Response
        """
        if platform is None:
            filter = 'name:{}'.format(name)
        else:
            filter = 'name:{},platforms:{}'.format(name, platform)

        search_params = {'filter': filter}
        response = self._query(search_params)

        return response
