Response
=========
Responses are wrapped up in the `pybomb.response` object::

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
