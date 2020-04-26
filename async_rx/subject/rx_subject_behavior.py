from typing import Optional

from ..protocol import Subject, SubjectHandler
from .rx_subject_replay import rx_subject_replay

__all__ = ["rx_subject_behavior"]


def rx_subject_behavior(subject_handler: Optional[SubjectHandler] = None) -> Subject:
    """Create a behavior subject.

    One of the variants of Subjects is the BehaviorSubject, which has a notion
    of "the current value".
    It stores the latest value emitted to its consumers, and whenever
    a new Observer subscribes, it will immediately receive the "current value"
    from the BehaviorSubject.

    BehaviorSubjects are useful for representing "values over time".
    For instance, an event stream of birthdays is a Subject,
    but the stream of a person's age would be a BehaviorSubject.

    Args:
        subject_handler (Optional[SubjectHandler]): optional suject handler callback

    Returns:
        (Subject): the subject

    """
    return rx_subject_replay(buffer_size=1, subject_handler=subject_handler)
