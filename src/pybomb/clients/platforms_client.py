"""Client for the Platforms resource of GiantBomb.

https://www.giantbomb.com/api/documentation#toc-0-30
"""
from typing import Any, Optional

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

    def quick_search(
        self,
        name: str,
        sort_by: Optional[str] = None,
        desc: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Search with a simplier API.

        This method allows you to search for a platform using only the name.

        Args:
            name: The name of the platform to search for
            sort_by: The field to sort the items in the reponse by.
                These will be validated against the availiable sort fields.
            desc: If sort direction is DESC or not (ASC). Defaults to True
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
             A PyBomb Response containg the results of the search
        """
        return self.search(filter_by={"name": name}, sort_by=sort_by, desc=desc)
