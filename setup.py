try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'version': '0.1.3',
    'long_description_markdown_filename': 'README.md',
    'license': "MIT",
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/PyBomb',
    'download_url': 'https://github.com/steveYeah/PyBomb/archive/v0.1.3.tar.gz',
    'keywords': ['giant', 'bomb', 'game', 'api', 'client'],
    'packages': ['pybomb', 'pybomb.clients'],
    'install_requires': [
        'nose',
        'requests',
        'setuptools-markdown',
    ]
}

setup(**config)
