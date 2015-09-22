"""
Base client to extend to create clients for endpoints of the GiantBomb API
"""
import requests
import pybomb.exceptions
import pybomb.response


class BaseClient(object):
    """
    Base class for API resource clients
    """

    URI_BASE = 'http://www.giantbomb.com/api/'
    RESPONSE_FORMAT_JSON = 'json'
    RESPONSE_FORMAT_XML = 'xml'
    RESPONSE_FIELD_MAP = None
    RESPONSE_STATUS_OK = 1

    RESOURCE_NAME = None

    SORT_ORDER_ASCENDING = 'asc'
    SORT_ORDER_DESCENDING = 'desc'

    PARAM_FILTER_FIELD = 0
    PARAM_SORT_FIELD = 1

    def __init__(self, api_key, default_format=RESPONSE_FORMAT_JSON):
        """
        :param api_key: string
        :param default_format: string
        """
        self._api_key = api_key
        self._default_format = default_format

    @property
    def api_key(self):
        """
        Giant Bomb API key

        :return: string
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """
        :param api_key: string
        """
        self._api_key = api_key

    @property
    def default_format(self):
        """
        Default API response type

        :return: string
        """
        return self._default_format

    def _validate_return_fields(self, return_fields):
        """
        :param return_fields: tuple
        :raises: pybomb.exceptions.InvalidReturnFieldException
        """
        for return_field in return_fields:
            if return_field not in self.RESPONSE_FIELD_MAP:
                raise pybomb.exceptions.InvalidReturnFieldException(
                    '"{0}" is an invalid return field'.format(return_field)
                )

    def _validate_sort_field(self, sort_by):
        """
        :param sort_by: string
        :raises: pybomb.exceptions.InvalidSortFieldException
        """
        if (sort_by not in self.RESPONSE_FIELD_MAP or
                not self.RESPONSE_FIELD_MAP[sort_by][self.PARAM_SORT_FIELD]):
            raise pybomb.exceptions.InvalidSortFieldException(
                '"{0}" is an invalid sort field'.format(sort_by)
            )

    def _validate_filter_fields(self, filter_by):
        """
        :param filter_by: dict
        :raises: pybomb.exceptions.InvalidFilterFieldException
        """
        for filter_field in filter_by:
            if (filter_field not in self.RESPONSE_FIELD_MAP or
                    not self.RESPONSE_FIELD_MAP[filter_field][self.PARAM_FILTER_FIELD]):
                raise pybomb.exceptions.InvalidFilterFieldException(
                    '"{0}" is an invalid filter field'.format(filter_field)
                )

    def _create_search_filter(self, filter_by):
        """
        :param filter_by:
        :return: dict
        """
        return ','.join(
            ['{0}:{1}'.format(key, value) for
             key, value in filter_by.items() if value is not None]
        )

    def _query(self, params):
        """
        :param params: dict
        :return: pybomb.clients.response
        """
        params['api_key'] = self._api_key

        if 'format' not in params:
            params['format'] = self._default_format

        response = self._query_api(params)
        self._validate_response(response)

        return pybomb.response.create_response(response)

    def _query_api(self, params):
        """
        :param params: dict
        :return: requests.models.Response
        """
        return requests.get(self.URI_BASE + self.RESOURCE_NAME, params=params)

    def _validate_response(self, response):
        """
        :param response: requests.models.Response
        :raises: pybomb.exceptions.InvalidResponseException
        :raises: pybomb.exceptions.BadRequestException
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise pybomb.exceptions.BadRequestException(str(http_error))

        response_data = response.json()
        if response_data['status_code'] != self.RESPONSE_STATUS_OK:
            raise pybomb.exceptions.InvalidResponseException(
                'Response code {0}: {1}'.format(
                    response_data['status_code'],
                    response_data['error']
                )
            )
