import pybomb.clients.base_client as base_client


class GameClient(base_client.BaseClient):

    RESOURCE_NAME = 'game'

    RESPONSE_FIELD_MAP = {
        'aliases': base_client.ResponseParam(True, False),
        'api_detail_url': base_client.ResponseParam(True, False),
        'characters': base_client.ResponseParam(True, False),
        'concepts': base_client.ResponseParam(True, False),
        'date_added': base_client.ResponseParam(True, False),
        'date_last_updated': base_client.ResponseParam(True, False),
        'deck': base_client.ResponseParam(True, False),
        'description': base_client.ResponseParam(True, False),
        'developers': base_client.ResponseParam(True, False),
        'expected_release_day': base_client.ResponseParam(True, False),
        'expected_release_month': base_client.ResponseParam(True, False),
        'expected_release_quarter': base_client.ResponseParam(True, False),
        'expected_release_year': base_client.ResponseParam(True, False),
        'first_appearance_characters': base_client.ResponseParam(True, False),
        'first_appearance_concepts': base_client.ResponseParam(True, False),
        'first_appearance_locations': base_client.ResponseParam(True, False),
        'first_appearance_objects': base_client.ResponseParam(True, False),
        'first_appearance_people': base_client.ResponseParam(True, False),
        'franchises': base_client.ResponseParam(True, False),
        'genres': base_client.ResponseParam(True, False),
        'id': base_client.ResponseParam(True, False),
        'image': base_client.ResponseParam(True, False),
        'images': base_client.ResponseParam(True, False),
        'killed_characters': base_client.ResponseParam(True, False),
        'locations': base_client.ResponseParam(True, False),
        'name': base_client.ResponseParam(True, False),
        'number_of_user_reviews': base_client.ResponseParam(True, False),
        'objects': base_client.ResponseParam(True, False),
        'original_game_rating': base_client.ResponseParam(False, True),
        'original_release_date': base_client.ResponseParam(True, False),
        'people': base_client.ResponseParam(True, False),
        'platforms': base_client.ResponseParam(True, False),
        'publishers': base_client.ResponseParam(True, False),
        'releases': base_client.ResponseParam(True, False),
        'reviews': base_client.ResponseParam(True, False),
        'similar_games': base_client.ResponseParam(True, False),
        'site_detail_url': base_client.ResponseParam(True, False),
        'themes': base_client.ResponseParam(True, False),
        'videos': base_client.ResponseParam(True, False),
    }

    def fetch(self, id_, return_fields=None):

        game_params = {'id': id_}

        if return_fields is not None:
            self._validate_return_fields(return_fields)
            field_list = ','.join(return_fields)

            game_params['field_list'] = field_list

        response = self._query(game_params, direct=True)

        return response
