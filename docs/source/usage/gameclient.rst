Game client
============
The GameClient is the client used to access the `game
endpoint <http://www.giantbomb.com/api/documentation#toc-0-16>`_ of the Giant Bomb API.

GameClient has one external method, `fetch`. `fetch` allows to retrieve all details of a game, using the GiantBomb ID,
allowing you to specify the required return fields.

fetch
------
Here is an example showing the full usage of the `fetch` method::

    import pybomb

    my_key = your_giant_bomb_api_key
    game_client = pybomb.GameClient(my_key)

    game_id = 1
    return_fields = ('id', 'name', 'platforms')

    response = game_client.fetch(game_id)

    print response.results
    print response.uri
    print response.num_page_results
    print response.num_total_results
