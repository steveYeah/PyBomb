"""Client for the Game resource of GiantBomb.

https://www.giantbomb.com/api/documentation#toc-0-16
"""
from typing import Dict, List, Union

from pybomb.clients.base.client import ResponseParam
from pybomb.clients.base.fetch_client import FetchClient
from pybomb.response import Response


class GameClient(FetchClient):
    """Client for the 'game' API resource."""

    RESOURCE_NAME = "game"

    RESPONSE_FIELD_MAP = {
        "aliases": ResponseParam(True, False),
        "api_detail_url": ResponseParam(True, False),
        "characters": ResponseParam(True, False),
        "concepts": ResponseParam(True, False),
        "date_added": ResponseParam(True, False),
        "date_last_updated": ResponseParam(True, False),
        "deck": ResponseParam(True, False),
        "description": ResponseParam(True, False),
        "developers": ResponseParam(True, False),
        "expected_release_day": ResponseParam(True, False),
        "expected_release_month": ResponseParam(True, False),
        "expected_release_quarter": ResponseParam(True, False),
        "expected_release_year": ResponseParam(True, False),
        "first_appearance_characters": ResponseParam(True, False),
        "first_appearance_concepts": ResponseParam(True, False),
        "first_appearance_locations": ResponseParam(True, False),
        "first_appearance_objects": ResponseParam(True, False),
        "first_appearance_people": ResponseParam(True, False),
        "franchises": ResponseParam(True, False),
        "genres": ResponseParam(True, False),
        "id": ResponseParam(True, False),
        "image": ResponseParam(True, False),
        "images": ResponseParam(True, False),
        "killed_characters": ResponseParam(True, False),
        "locations": ResponseParam(True, False),
        "name": ResponseParam(True, False),
        "number_of_user_reviews": ResponseParam(True, False),
        "objects": ResponseParam(True, False),
        "original_game_rating": ResponseParam(False, True),
        "original_release_date": ResponseParam(True, False),
        "people": ResponseParam(True, False),
        "platforms": ResponseParam(True, False),
        "publishers": ResponseParam(True, False),
        "releases": ResponseParam(True, False),
        "reviews": ResponseParam(True, False),
        "similar_games": ResponseParam(True, False),
        "site_detail_url": ResponseParam(True, False),
        "themes": ResponseParam(True, False),
        "videos": ResponseParam(True, False),
    }

    def fetch(self, id_: int, return_fields: List = None) -> Response:
        """Fetch details of a game by ID.

        Args:
            id_: The ID of the game
            return_fields: A list of fields to be returned by the response.
                These will be validated against the availiable return fields.
                The default is to return everything

        Returns:
            A Pybomb Respose object containing the details of the requested game
        """
        game_params: Dict[str, Union[str, int]] = {"id": id_}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ",".join(return_fields)

            game_params["field_list"] = field_list

        response = self._query(game_params)

        return response
