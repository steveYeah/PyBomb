Clients
=======
All clients are instantiated in the same way. Each take an API key and a response type.

API key
-------
This is the Giant Bomb API key. You can acquire one on the `Giant Bomb site <http://www.giantbomb.com/api/>`_.

Response type
-------------
Giant bomb supports `JSON` and `XML` response types. The default for all the clients is `JSON`

Example
-------
Here is an example using the GamesClient::

    import pybomb
    from pybomb.clients.client import Client

    # Using default `JSON` return type
    my_key = "your_giant_bomb_api_key"
    games_client = pybomb.GamesClient(api_key=my_key)

    # Using `XML` return type
    games_client = pybomb.GamesClient(
        api_key=my_key,
        default_format=Client.RESPONSE_FORMAT_XML
    )

Endpoint clients
----------------
.. toctree::
   :maxdepth: 1

   gamesclient
   gameclient
