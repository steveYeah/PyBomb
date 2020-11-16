"""A library of clients for the main resources of the GiantBomb API.

http://www.giantbomb.com/api/documentation#toc-0-1
"""
try:
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

from pybomb.clients.game_client import GameClient
from pybomb.clients.games_client import GamesClient
from pybomb.clients.platforms_client import PlatformsClient
from pybomb.exceptions import (
    BadRequestException,
    ClientException,
    InvalidFilterFieldException,
    InvalidResponseException,
    InvalidReturnFieldException,
    InvalidSortFieldException,
    PybombException,
)

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

# Platform ID's
PS1 = 22
PS2 = 19
PS3 = 35
PS4 = 146

XBOX = 32
XBOX_360 = 20
XBOX_ONE = 145

MAC = 17
PC = 94
