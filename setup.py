try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'version': '0.1.1',
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/PyBomb',
    'download_url': 'https://github.com/steveYeah/PyBomb/archive/v0.1.1.tar.gz',
    'keywords': ['giant', 'bomb', 'game', 'api', 'client],
    'packages': ['pybomb', 'pybomb.clients'],
    'install_requires': [
        'nose',
        'requests',
    ]
}

setup(**config)
