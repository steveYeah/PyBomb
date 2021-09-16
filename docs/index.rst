PyBomb
======
PyBomb is a collection of simple clients for the `Giant Bomb API <http://www.giantbomb.com/api/>`_. Often API clients are just one big
class with a different method for each of the endpoints. Here we have created each endpoint as a separate
class. Why? Well, there is a lot of endpoints to the GiantBomb API, and you probably don't use all of them in
your project. Keeping them separate helps to make the imports light and the code more maintainable.

Here's an example of the Games endpoint::

   import pybomb

   my_key = your_giant_bomb_api_key
   games_client = pybomb.GamesClient(my_key)

   return_fields = ('id', 'name', 'platforms')
   limit = 10
   offset = 5
   sort_by = 'name'
   filter_by = {'platforms': pybomb.PS3}

   response = games_client.search(
     filter_by=filter_by,
     return_fields=return_fields,
     sort_by=sort_by,
     desc=True,
     limit=limit,
     offset=offset
   )

   print response.results
   print response.uri
   print response.num_page_results
   print response.num_total_results



Alternatively you can use the client factory to build all the clients from a single location, meaning you only need to supply the API key once::

    import pybomb

    my_key = your_giant_bomb_api_key
    client_factory = pybomb.ClientFactory(my_key)
    games_client = client_factory.build("games")

    return_fields = ('id', 'name', 'platforms')
    limit = 10
    offset = 5
    sort_by = 'name'
    filter_by = {'platforms': pybomb.PS3}

    response = games_client.search(
    filter_by=filter_by,
    return_fields=return_fields,
    sort_by=sort_by,
    desc=True,
    limit=limit,
    offset=offset
    )

    print response.results
    print response.uri
    print response.num_page_results
    print response.num_total_results

Usage
-----
Examples of how to use the PyBomb clients, and response object.

.. toctree::
   :maxdepth: 1

   usage/clients
   usage/response

API Documentation
-----------------
All the API documentation.

.. toctree::
   :maxdepth: 2

   api/clients
   api/exceptions
   api/factory
   api/response
