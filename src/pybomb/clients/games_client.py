"""Client for the Games resource of GiantBomb.

https://www.giantbomb.com/api/documentation#toc-0-17
"""
from typing import Any, Dict, List, Optional, Union

from pybomb.clients.base_client import BaseClient, ResponseParam
from pybomb.response import Response


class GamesClient(BaseClient):
    """Client for the 'games' API resource."""

    RESOURCE_NAME = "games"

    RESPONSE_FIELD_MAP = {
        "aliases": ResponseParam(True, False),
        "api_detail_url": ResponseParam(False, False),
        "date_added": ResponseParam(True, True),
        "date_last_updated": ResponseParam(True, True),
        "deck": ResponseParam(False, False),
        "description": ResponseParam(False, False),
        "expected_release_month": ResponseParam(True, False),
        "expected_release_quarter": ResponseParam(True, False),
        "expected_release_year": ResponseParam(True, False),
        "id": ResponseParam(True, True),
        "image": ResponseParam(False, False),
        "name": ResponseParam(True, True),
        "number_of_user_reviews": ResponseParam(True, True),
        "original_game_rating": ResponseParam(False, True),
        "original_release_date": ResponseParam(True, True),
        "platforms": ResponseParam(True, False),
        "site_detail_url": ResponseParam(False, False),
    }

    def search(
        self,
        filter_by: Dict[str, Any],
        return_fields: List = None,
        sort_by: Optional[str] = None,
        desc: bool = True,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Response:
        """Full search of games resource.

        Supports all search fields available in API
        http://www.giantbomb.com/api/documentation#toc-0-17

        Args:
            filter_by: A map of fields to filter the search by. These will
                be validated against the availiable search fields
            return_fields: A list of fields to be returned by the response.
                These will be validated against the availiable return fields.
                The default is to return everything
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True
            limit: The max number of items to request
            offset: The start offset for the return items, based on the given sort.

        Returns:
             A PyBomb Response containg the results of the search
        """
        self._validate_filter_fields(filter_by)
        search_filter = self._create_search_filter(filter_by)

        search_params: Dict[str, Union[str, int]] = {"filter": search_filter}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ",".join(return_fields)

            search_params["field_list"] = field_list

        if sort_by is not None:
            self._validate_sort_field(sort_by)

            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params["sort"] = "{0}:{1}".format(sort_by, direction)

        if limit is not None:
            search_params["limit"] = int(limit)

        if offset is not None:
            search_params["offset"] = int(offset)

        response = self._query(search_params)

        return response

    def quick_search(
        self,
        name: str,
        platform: Optional[int] = None,
        sort_by: Optional[str] = None,
        desc: bool = True,
    ) -> Response:
        """Search with a simplier API.

        This method allows you to search for a game using only the title and
        the platform.

        Args:
            name: The name of the game to search for
            platform: The platform ID that the game is required to have.
                When set to None no platform filters will be added. Defaults to None
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True

        Returns:
             A PyBomb Response containg the results of the search
        """
        if platform is None:
            query_filter = "name:{0}".format(name)
        else:
            query_filter = "name:{0},platforms:{1}".format(name, platform)

        search_params: Dict[str, Union[str, int]] = {"filter": query_filter}

        if sort_by is not None:
            self._validate_sort_field(sort_by)

            if desc:
                direction = self.SORT_ORDER_DESCENDING
            else:
                direction = self.SORT_ORDER_ASCENDING

            search_params["sort"] = "{0}:{1}".format(sort_by, direction)

        response = self._query(search_params)

        return response
