import requests


class BaseClient(object):

    # @todo add the error codes here...
    # @todo implement validate response

    URI_BASE = 'http://www.giantbomb.com/api/{}'
    RESPONSE_FORMAT_JSON = 'json'
    RESPONSE_FORMAT_XML = 'xml'

    def __init__(self, api_key, default_format=RESPONSE_FORMAT_JSON):
        """
        :param api_key: string
        :param default_format: string
        """
        self.api_key = api_key
        self.default_format = default_format

    def _validate_return_fields(self, return_fields):
        """
        :param return_fields: tuple
        :raises: Exception
        """
        for return_field in return_fields:
            if return_field not in self.RESPONSE_FIELDS:
                raise Exception('Invalid return field specified: {}.format(return_field)')

    def _validate_sort_field(self, sort_by):
        """
        :param sort_by: tuple
        :raises: Exception
        """
        if (
            sort_by[0] not in self.RESPONSE_FIELDS or
            not self.RESPONSE_FIELDS[sort_by[0]][self.SORT_FIELD]
        ):
            raise Exception('Invalid sort field specified: {}'.format(sort_by[0]))

    def _validate_filter_fields(self, filter_by):
        """
        :param filter_by: dict
        :raise: Exception
        """
        for filter_field in filter_by:
            if (
                filter_field not in self.RESPONSE_FIELDS or
                not self.RESPONSE_FIELDS[filter_field][self.FILTER_FIELD]
            ):
                raise Exception('Invalid filter field specified: {}'.format(filter_field))

    def _create_search_filter(self, filter_by):
        """
        :param filter_by:
        :return:
        """
        return ','.join(
            ['{}:{}'.format(key, value) for key, value in filter_by.iteritems()]
        )

    def _query(self, params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        params['api_key'] = self.api_key

        if 'format' not in params:
            params['format'] = self.default_format

        response = requests.get(self.URI_BASE.format(self.RESOURCE_NAME), params)
        response.raise_for_status()

        return response

    def _validate_response(self, response):
        # test for the status_code for responses and throw correct exception
        pass


class GamesClient(BaseClient):

    RESOURCE_NAME = 'games'

    FILTER_FIELD = 0
    SORT_FIELD = 1

    RESPONSE_FIELDS = {
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
            'sort': '{}:{}'.format(sort_by[0], sort_by[1]),
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
            filter = "name:{}".format(name)
        else:
            filter = "name:{},platforms:{}".format(name, platform)

        search_params = {'filter': filter}
        response = self._query(search_params)

        return response
