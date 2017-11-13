"""
Client for the Games resource of GiantBomb
http://www.giantbomb.com/api/documentation#toc-0-15
"""
from pybomb.clients.base_client import BaseClient, ResponseParam


class GamesClient(BaseClient):
    """
    Client for the 'games' API resource
    """

    RESOURCE_NAME = 'games'

    RESPONSE_FIELD_MAP = {
        'aliases': ResponseParam(True, False),
        'api_detail_url': ResponseParam(False, False),
        'date_added': ResponseParam(True, True),
        'date_last_updated': ResponseParam(True, True),
        'deck': ResponseParam(False, False),
        'description': ResponseParam(False, False),
        'expected_release_month': ResponseParam(True, False),
        'expected_release_quarter': ResponseParam(True, False),
        'expected_release_year': ResponseParam(True, False),
        'id': ResponseParam(True, True),
        'image': ResponseParam(False, False),
        'name': ResponseParam(True, True),
        'number_of_user_reviews': ResponseParam(True, True),
        'original_game_rating': ResponseParam(False, True),
        'original_release_date': ResponseParam(True, True),
        'platforms': ResponseParam(True, False),
        'site_detail_url': ResponseParam(False, False),
    }

    def search(
        self, filter_by, return_fields=None, sort_by=None, desc=True,
        limit=None, offset=None
    ):
        """
        Full search of games resource, supporting all search fields
        available in API
        http://www.giantbomb.com/api/documentation#toc-0-15

        :param filter_by: dict
        :param return_fields: tuple
        :param sort_by: string
        :param desc: bool
        :param limit: int
        :param offset: int
        :return: pybomb.clients.Response
        """
        self._validate_filter_fields(filter_by)
        search_filter = self._create_search_filter(filter_by)

        search_params = {'filter': search_filter}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ','.join(return_fields)

            search_params['field_list'] = field_list

        if sort_by is not None:
            self._validate_sort_field(sort_by)

            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params['sort'] = '{0}:{1}'.format(sort_by, direction)

        if limit is not None:
            search_params['limit'] = int(limit)

        if offset is not None:
            search_params['offset'] = int(offset)

        response = self._query(search_params)

        return response

    def quick_search(self, name, platform=None, sort_by=None, desc=True):
        """
        Quick search method that allows you to search for a game using only the
        title and the platform

        :param name: string
        :param platform: int
        :param sort_by: string
        :param desc: bool
        :return: pybomb.clients.Response
        """
        if platform is None:
            query_filter = 'name:{0}'.format(name)
        else:
            query_filter = 'name:{0},platforms:{1}'.format(name, platform)

        search_params = {'filter': query_filter}

        if sort_by is not None:
            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params['sort'] = '{0}:{1}'.format(sort_by, direction),

        response = self._query(search_params)

        return response
