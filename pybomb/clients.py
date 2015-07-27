import requests


class BaseClient(object):

    # @todo add the error codes here...
    # @todo implement validate response

    URI_BASE = 'http://www.giantbomb.com/api/{}'
    RESPONSE_FORMAT_JSON = 'json'
    RESPONSE_FORMAT_XML = 'xml'

    def __init__(self, api_key, default_format=RESPONSE_FORMAT_JSON):
        self.api_key = api_key
        self.default_format = default_format

    def _query(self, params):
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
        # validate return fields
        for return_field in return_fields:
            if return_field not in self.RESPONSE_FIELDS:
                raise Exception('Invalid return field specified: {}.format(return_field)')

        # validate sort
        if (
            sort_by[0] not in self.RESPONSE_FIELDS or
            not self.RESPONSE_FIELDS[sort_by[0]][self.SORT_FIELD]
        ):
            raise Exception('Invalid sort field specified: {}'.format(sort_by[0]))

        # validate filter_by
        for filter_field in filter_by:
            if (
                filter_field not in self.RESPONSE_FIELDS or
                not self.RESPONSE_FIELDS[filter_field][self.FILTER_FIELD]
            ):
                raise Exception('Invalid filter field specified: {}'.format(filter_field))

        search_filter = ','.join(
            ['{}:{}'.format(key, value) for key, value in filter_by.iteritems()]
        )
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
        if platform is None:
            filter = "name:{}".format(name)

        else:
            filter = "name:{},platforms:{}".format(name, platform)

        search_params = {'filter': filter}
        response = self._query(search_params)
        return response
