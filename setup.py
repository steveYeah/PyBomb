try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'version': '0.1',
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': '',
    'download_url': '',
    'packages': ['pybomb'],
    'install_requires': [
        'nose',
        'requests',
    ]
}

setup(**config)
