from codecs import open
import os
from setuptools import setup, find_packages

version = '0.2.0'
download_url = (
    'https://github.com/steveYeah/PyBomb/archive/v{0}.tar.gz'.format(version)
)

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name='pybomb',
    description='Clients for the Giant Bomb API',
    packages=find_packages(exclude=['test', 'test.*']),
    version=version,
    long_description=readme,
    license="MIT",
    author='Steve Hutchins',
    author_email='hutchinsteve@gmail.com',
    url='https://github.com/steveYeah/PyBomb',
    download_url=download_url,
    keywords=(
        'giantbomb'
        'giant',
        'bomb',
        'game',
        'api',
        'client'
    ),
    install_requires=(
        'requests',
    ),
    extras_require={
        'dev': (
            'pytest',
            'pycodestyle',
            'flake8',
            'sphinx',
            'sphinx-autobuild',
        ),
    },
    classifiers=(
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
