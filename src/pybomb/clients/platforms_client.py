"""Client for the Platforms resource of GiantBomb.

https://www.giantbomb.com/api/documentation#toc-0-30
"""
from typing import Any, Dict, List, Optional, Union

from pybomb.clients.base.client import ResponseParam
from pybomb.clients.base.search_client import SearchClient
from pybomb.response import Response


class PlatformsClient(SearchClient):
    """Client for the 'platforms' API resource."""

    RESOURCE_NAME = "platforms"

    RESPONSE_FIELD_MAP = {
        "abbreviation": ResponseParam(True, True),
        "api_detail_url": ResponseParam(False, False),
        "company": ResponseParam(True, False),
        "date_added": ResponseParam(True, True),
        "date_last_updated": ResponseParam(True, True),
        "deck": ResponseParam(False, False),
        "description": ResponseParam(False, False),
        "guid": ResponseParam(False, False),
        "id": ResponseParam(True, True),
        "image": ResponseParam(False, False),
        "image_tags": ResponseParam(False, False),
        "install_base": ResponseParam(True, True),
        "name": ResponseParam(True, True),
        "online_support": ResponseParam(True, True),
        "original_price": ResponseParam(True, True),
        "release_date": ResponseParam(True, True),
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
        """Full search of platforms resource.

        Supports all search fields available in API
        http://www.giantbomb.com/api/documentation#toc-0-30

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
        self, name: str, sort_by: Optional[str] = None, desc: bool = True,
    ) -> Response:
        """Search with a simplier API.

        This method allows you to search for a platform using only the name.

        Args:
            name: The name of the platform to search for
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True

        Returns:
             A PyBomb Response containg the results of the search
        """
        query_filter = "name:{0}".format(name)
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
