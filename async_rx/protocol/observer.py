"""Observer utilities."""
from collections import namedtuple
from typing import Any, NoReturn

from .definition import CompleteHandler, ErrorHandler, NextHandler, Observer

__all__ = ["rx_observer", "default_on_completed", "default_error", "ignore_error_handler"]


_ObserverDefinition = namedtuple("Observer", ["on_next", "on_error", "on_completed"])
"""Implements Observer Protocol."""


async def default_on_completed() -> None:
    """Default on complet handler.

    No operation.

    Returns:
        (None): nothing

    """
    pass


async def default_error(err: Any) -> NoReturn:
    """Always raise error.

    It's our default error handler implementation.
    """
    if isinstance(err, BaseException):
        raise err

    raise Exception(err)


async def ignore_error_handler(err: Any) -> None:
    """Always ignore error."""
    pass


def rx_observer(on_next: NextHandler, on_error: ErrorHandler = default_error, on_completed: CompleteHandler = default_on_completed) -> Observer:
    """Return an observer.

    The underlying implementation use an named tuple.

    Args:
        on_next (NextHandler): on_next handler which process items
        on_error (ErrorHandler): on_error handler (default with default_error
            which raise Exception)
        on_completed (CompleteHandler): on_completed handler (default with noop)

    Returns:
        (Observer): an Observer

    """
    return _ObserverDefinition(on_next=on_next, on_error=on_error, on_completed=on_completed)
