Platforms client
================
The PlatformsClient is the client used to access the `platforms
endpoint <http://www.giantbomb.com/api/documentation#toc-0-30>`_ of the Giant Bomb API.

PlatformsClient has two external methods.
`search` offers a full API to the endpoint, allowing you to specify all fields,
filters and return parameters. There is also a `quick_search` that allows you
to search just using a platform name.

search
------
Here is an example showing the full usage of the `search` method::

    import pybomb

    my_key = your_giant_bomb_api_key
    platforms_client = pybomb.PlatformsClient(my_key)

    return_fields = ('id', 'name')
    limit = 10
    offset = 5
    sort_by = 'name'
    filter_by = {'company': 'sony'}

    response = platforms_client.search(
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

quick_search
------------
Here is an example showing the full usage of the `quick_search` method::

    import pybomb

    my_key = your_giant_bomb_api_key
    platforms_client = pybomb.PlatformsClient(my_key)

    response = platforms_client.quick_search(
      name='playstation',
      sort_by='original_release_date',
      desc=True
    )

    print response.results
    print response.uri
    print response.num_page_results
    print response.num_total_results
