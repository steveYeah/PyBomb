try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def markdown_description(file_name):
    desc = pypandoc.convert(file_name, 'rst', format='md')
    return desc


try:
    import pypandoc
    long_description = markdown_description('README.md')
except ImportError:
    long_description = 'See README.md'


config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'version': '0.1.4',
    'long_description': long_description,
    'license': "MIT",
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/PyBomb',
    'download_url': 'https://github.com/steveYeah/PyBomb/archive/v0.1.4.tar.gz',
    'keywords': ['giant', 'bomb', 'game', 'api', 'client'],
    'packages': ['pybomb', 'pybomb.clients'],
    'install_requires': [
        'nose',
        'requests',
    ]
}

setup(**config)
