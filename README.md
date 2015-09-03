PyBomb
==============
[![PyPi version](https://img.shields.io/pypi/v/pybomb.svg?)](http://badge.fury.io/py/pybomb)
[![PyPi downloads](https://img.shields.io/pypi/dm/pybomb.svg?)](ttps://pypi.python.org/pypi/pybomb)


Simple client for the Giant Bomb API.
[Giant Bomb Docs](http://www.giantbomb.com/api/)

This will go into version 1.0 when all resources are supported.

###Currently Supported Resources:
* games

Install
-------
```
pip install pybomb
```

Examples
--------
####GamesClient - search
```
import pybomb

my_key = your_giant_bomb_api_key
games_client = pybomb.GamesClient(my_key)

return_fields = ('id', 'name', 'platforms')
limit = 10
offset = 5
sort_by = 'name'
filter_by = {'platforms': pybomb.PS3}

response = games_client.search(
  filter_by, return_fields, sort_by, desc=True, limit=limit, offset=offset
)

print response.results
print response.uri
print response.num_page_results
print response.num_total_results
```

####GamesClient - quick_search
```
import pybomb

my_key = your_giant_bomb_api_key
games_client = pybomb.GamesClient(my_key)

response = games_client.quick_search(
  'call of duty', platform=pybomb.PS3, sort_by='original_release_date', desc=True
)

print response.results
print response.uri
print response.num_page_results
print response.num_total_results
```
