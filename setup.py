try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def markdown_description(file_name):
    desc = pypandoc.convert(file_name, 'rst', format='md')
    return desc


version = '0.1.5'


try:
    import pypandoc
    long_description = markdown_description('README.md')
except ImportError:
    long_description = 'See README.md'


config = {
    'name': 'pybomb',
    'description': 'Client for the Giant Bomb API',
    'version': '{0}'.format(version),
    'long_description': long_description,
    'license': "MIT",
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/PyBomb',
    'download_url': 'https://github.com/steveYeah/PyBomb/archive/v{0}.tar.gz'.format(version),
    'keywords': ['giant', 'bomb', 'game', 'api', 'client'],
    'packages': ['pybomb', 'pybomb.clients'],
    'install_requires': [
        'requests',
    ]
}

setup(**config)
