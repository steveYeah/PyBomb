"""Client for the Games resource of GiantBomb.

https://www.giantbomb.com/api/documentation#toc-0-17
"""
from typing import Any, Dict, Optional, Union

from pybomb.clients.base.client import ResponseParam
from pybomb.clients.base.search_client import SearchClient
from pybomb.response import Response


class GamesClient(SearchClient):
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

    def quick_search(
        self,
        name: str,
        sort_by: Optional[str] = None,
        desc: bool = True,
        platform: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
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
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
             A PyBomb Response containg the results of the search
        """
        filter_by: Dict[str, Union[str, int]] = {"name": name}
        if platform is not None:
            filter_by["platforms"] = platform

        return self.search(filter_by=filter_by, sort_by=sort_by, desc=desc)
