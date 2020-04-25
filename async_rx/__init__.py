"""async-rx definition."""
from pkg_resources import DistributionNotFound, get_distribution

import protocol as _protocol
from .protocol.definition import *  # noqa: 403
from .protocol.observer import *  # noqa: 403

from .subject import *  # noqa: 403
from .multicast import *  # noqa: 403
from .observable import *  # noqa: 403


__all__ = [
    *_protocol.definition.__all__,
    *_protocol.observer.__all__,
    *subject.__all__,  # noqa: F405
    *multicast.__all__,  # noqa: F405
    *observable.__all__,  # noqa: F405
]

try:
    __version__ = get_distribution('async_rx').version
except DistributionNotFound:
    __version__ = '(local)'
