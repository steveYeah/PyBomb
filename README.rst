.. image:: https://img.shields.io/travis/steveYeah/PyBomb.svg?branch=master
   :target: https://travis-ci.org/steveYeah/PyBomb

PyBomb
==============

.. pull-quote::
  Simple clients for the Giant Bomb API.
  http://www.giantbomb.com/api/

This will go into version 1.0 when all resources are supported.

**Currently Supported Resources**:

* games
* game

Install
-------

.. code-block:: shell

   pip install pybomb


Examples
--------
**GamesClient - search**

.. code-block::

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

**GamesClient - quick_search**

.. code-block::

  import pybomb

  my_key = your_giant_bomb_api_key
  games_client = pybomb.GamesClient(my_key)

  response = games_client.quick_search(
    name='call of duty',
    platform=pybomb.PS3,
    sort_by='original_release_date',
    desc=True
  )

  print response.results
  print response.uri
  print response.num_page_results
  print response.num_total_results

More examples for other clients can be found in the documentation
https://pybomb.readthedocs.org

To see a working example of Pybomb, take a look at the example project GameSearch
https://github.com/steveYeah/gamesearch
