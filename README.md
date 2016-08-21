PyBomb
==============
[![PyPi version](https://img.shields.io/pypi/v/pybomb.svg?)](http://badge.fury.io/py/pybomb)
[![PyPi status](https://img.shields.io/travis/steveYeah/PyBomb.svg?)](https://travis-ci.org/steveYeah/PyBomb)

Simple client for the Giant Bomb API.
[Giant Bomb Docs](http://www.giantbomb.com/api/)

This will go into version 1.0 when all resources are supported.

###Currently Supported Resources:
* games

Install
-------
```sh
pip install pybomb
```

Examples
--------
####GamesClient - search
```python
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
```

####GamesClient - quick_search
```python
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
```
