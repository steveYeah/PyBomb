#Games client
The `GamesClient` is used to access the [games endpoint of the Giant Bomb API](http://www.giantbomb.com/api/documentation#toc-0-15).

###Methods
There are two main methods; `search` and `quick_search`.

####search
The `search` method allows full access to all the fields and filters described in the API documentation. Below 
is a full example using all the possible parameters:

    import pybomb
    
    my_key = your_giant_bomb_api_key
    games_client = pybomb.GamesClient(my_key)
    
    return_fields = ('id', 'name', 'platforms')
    limit = 10
    offset = 5
    sort_by = 'name'
    filter_by = {'platforms': pybomb.PS3}
    
    response = games_client.search(
      filter_by, 
      return_fields, 
      sort_by, 
      desc=True, 
      limit=limit, 
      offset=offset
    )
    
    print response.results
    print response.uri
    print response.num_page_results
    print response.num_total_results

####quick_search
`quick_search` is a convenience method that allows you to just search games by name and platform. The example 
below shows usage of all the possible params:

    import pybomb
    
    my_key = your_giant_bomb_api_key
    games_client = pybomb.GamesClient(my_key)
    
    response = games_client.quick_search(
      'call of duty', 
      platform=pybomb.PS3, 
      sort_by='original_release_date', 
      desc=True
    )
    
    print response.results
    print response.uri
    print response.num_page_results
    print response.num_total_results
     