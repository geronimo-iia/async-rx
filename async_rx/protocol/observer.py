"""Observer utilities."""
from collections import namedtuple
from typing import Any, NoReturn, Optional

from .definition import CompleteHandler, ErrorHandler, NextHandler, Observer

__all__ = ["rx_observer", "rx_observer_from", "default_on_completed", "default_error", "ignore_error_handler"]


_ObserverDefinition = namedtuple("Observer", ["on_next", "on_error", "on_completed"])
"""Implements Observer Protocol."""


async def default_on_completed() -> None:  # pragma: no cover
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


async def ignore_error_handler(err: Any) -> None:  # pragma: no cover
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


def rx_observer_from(
    observer: Observer, on_next: Optional[NextHandler] = None, on_error: Optional[ErrorHandler] = None, on_completed: Optional[CompleteHandler] = None
) -> Observer:
    """Build an observer from another one.

    Args:
        observer (Observer): the observer to override
        on_next (Optional[NextHandler]): override on_next handler if set
        on_error (Optional[ErrorHandler]): override on_error handler if set
        on_completed (Optional[CompleteHandler]): override on_completed handler if set

    Returns:
        (Observer): an Observer

    """
    return rx_observer(
        on_next=on_next if on_next else observer.on_next,
        on_error=on_error if on_error else observer.on_error,
        on_completed=on_completed if on_completed else observer.on_completed,
    )
