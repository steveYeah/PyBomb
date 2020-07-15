![Tests](https://github.com/steveYeah/PyBomb/workflows/Tests/badge.svg)
![Coverage](https://github.com/steveYeah/PyBomb/workflows/Coverage/badge.svg)
![Release Drafter](https://github.com/steveYeah/PyBomb/workflows/Release%20Drafter/badge.svg)
![TestPyPi](https://github.com/steveYeah/PyBomb/workflows/TestPyPi/badge.svg)
![Release](https://github.com/steveYeah/PyBomb/workflows/Release/badge.svg)

[![Codecov](https://codecov.io/gh/steveYeah/PyBomb/branch/master/graph/badge.svg)](https://codecov.io/gh/steveYeah/PyBomb)
[![PyPI](https://img.shields.io/pypi/v/PyBomb.svg)](https://pypi.org/project/PyBomb/)
[![Read the Docs](https://readthedocs.org/projects/pybomb/badge/)](https://pybomb.readthedocs.io/)
# PyBomb

>

This will go into version 1.0 when all resources are supported.

**Currently Supported Resources**:

  - games
  - game

## Install

``` shell
pip install pybomb
```

## Examples

To see a working example of Pybomb, take a look at the example project
PyBomb-demo <https://github.com/steveYeah/PyBomb-demo>

**GamesClient - search**

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

**GamesClient - quick\_search**

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

## Documentation

The full documentation, including more examples can be found at
<https://pybomb.readthedocs.org>
