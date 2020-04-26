"""Subject utilities."""
from collections import namedtuple

from .definition import CompleteHandler, ErrorHandler, NextHandler, Subject, SubjectEventHandler, SubjectHandler, Subscribe
from .observer import default_error, default_on_completed

__all__ = ["subject_handler", "subject"]

_SubjectDefinition = namedtuple("Subject", ["subscribe", "on_next", "on_error", "on_completed"])
"""Implements Subject Protocol."""

_SubjectHandlerDefinition = namedtuple("SubjectHandler", ["on_subscribe", "on_unsubscribe"])
"""Implements SubjectHandler Protocol."""


def subject(
    subscribe: Subscribe, on_next: NextHandler, on_error: ErrorHandler = default_error, on_completed: CompleteHandler = default_on_completed
) -> Subject:
    """Build a subject.

    The underlying implementation use an named tuple.

    Args:
        subscribe (Subscribe): subscription handler.
        on_next (NextHandler): on_next handler which process items
        on_error (ErrorHandler): on_error handler (default with default_error
            which raise Exception)
        on_completed (CompleteHandler): on_completed handler (default with noop)

    Returns:
        (Subject): a subject

    """
    return _SubjectDefinition(subscribe=subscribe, on_next=on_next, on_error=on_error, on_completed=on_completed)


def subject_handler(on_subscribe: SubjectEventHandler, on_unsubscribe: SubjectEventHandler) -> SubjectHandler:
    """Create a SubjectHandler.

    Args:
        on_subscribe (SubjectEventHandler): on subscribe event handler
        on_unsubscribe (SubjectEventHandler): on unsubscribe event handler
    Returns:
        (SubjectHandler): a SubjectHandler instance.

    """
    return _SubjectHandlerDefinition(on_subscribe=on_subscribe, on_unsubscribe=on_unsubscribe)
