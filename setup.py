import os


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'long_description': read('README.md'),
    'version': '0.1.1',
    'license': "MIT",
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/PyBomb',
    'download_url': 'https://github.com/steveYeah/PyBomb/archive/v0.1.1.tar.gz',
    'keywords': ['giant', 'bomb', 'game', 'api', 'client'],
    'packages': ['pybomb', 'pybomb.clients'],
    'install_requires': [
        'nose',
        'requests',
    ]
}

setup(**config)
