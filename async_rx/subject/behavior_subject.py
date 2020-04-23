from typing import Any, Optional

from ..protocol import Observer, Subject, SubjectDefinition, SubjectHandler, Subscription
from .subject import subject

__all__ = ["behavior_subject"]


def behavior_subject(subject_handler: Optional[SubjectHandler] = None) -> Subject:
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
    _last_item: Any = None

    _subject = subject(subject_handler=subject_handler)

    async def _on_next(item: Any) -> None:
        nonlocal _last_item, _subject

        _last_item = item
        await _subject.on_next(item)

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _last_item, _subject

        subscription = await _subject.subscribe(an_observer)

        if _last_item is not None:
            await an_observer.on_next(_last_item)

        return subscription

    return SubjectDefinition(subscribe=_subscribe, on_next=_on_next, on_error=_subject.on_error, on_completed=_subject.on_completed)
