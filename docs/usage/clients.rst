Clients
=======
All clients are instantiated in the same way, and only require an API key.

API key
-------
This is the Giant Bomb API key. You can acquire one on the `Giant Bomb site <http://www.giantbomb.com/api/>`_.

Example
-------
Here is an example using the GamesClient::

    import pybomb

    my_key = "your_giant_bomb_api_key"
    games_client = pybomb.GamesClient(api_key=my_key)

Endpoint clients
----------------
.. toctree::
   :maxdepth: 1

   gamesclient
   gameclient
