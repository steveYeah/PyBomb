[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C826VYD)

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
  - platforms

## Support OSS, and me :)
If you find this project useful, please feel free to [buy me a coffee](https://ko-fi.com/steveyeah)

## Install

``` shell
pip install pybomb
```

## Examples

To see a working example of Pybomb, take a look at the example project
[PyBomb-demo](https://github.com/steveYeah/PyBomb-demo)

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
[readthedocs](https://pybomb.readthedocs.org)

## Contributing

This project uses [Poetry](https://python-poetry.org/) and [Nox](https://nox.thea.codes/en/stable/) so make sure you have those setup!

Whilst working you can use

```shell
$ nox -rs tests
```
to run the tests, but once you have finished, make sure to run all of nox before making a PR

```shell
$ nox
```

This project also uses [Pytest](https://docs.pytest.org/en/stable/) for tests, and we aim for 100% test coverage. The build will fail when the coverage is less than this, but feel free to use `# pragma: no cover` if it makes sense to do so (although this should be very rare). [Mypy](http://mypy-lang.org/) is also used, and we even use [typeguard](https://typeguard.readthedocs.io/en/latest/) so typing is important here!

I am always happy to help where I can and I try to be as responsive as possible to PRs. Email me if I am slow, or if you need any help!
