from typing import Optional

from ..protocol import CompleteHandler, ErrorHandler, NextHandler, Subject, Subscribe, subject

__all__ = ["rx_subject_from"]


def rx_subject_from(
    a_subject: Subject,
    subscribe: Optional[Subscribe] = None,
    on_next: Optional[NextHandler] = None,
    on_error: Optional[ErrorHandler] = None,
    on_completed: Optional[CompleteHandler] = None,
) -> Subject:
    """Build a subject from another one by override some function.

    Args:
        a_subject (Subject): the source subject
        subscribe (Optional[Subscribe]): override subscribe if set
        on_next (Optional[NextHandler]): override on_next if set
        on_error (Optional[ErrorHandler]): override on_error if set
        on_completed (Optional[CompleteHandler]): override on_completed if set

    Returns;
        (Subject): a new subject

    """
    return subject(
        subscribe=subscribe if subscribe else a_subject.subscribe,
        on_next=on_next if on_next else a_subject.on_next,
        on_error=on_error if on_error else a_subject.on_error,
        on_completed=on_completed if on_completed else a_subject.on_completed,
    )
