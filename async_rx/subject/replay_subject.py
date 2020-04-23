from collections import deque
from typing import Any, Deque, Optional, NoReturn

from ..protocol import Observer, Subject, SubjectDefinition, SubjectHandler, Subscription
from .subject import subject

__all__ = ["replay_subject"]


def replay_subject(buffer_size: int, subject_handler: Optional[SubjectHandler] = None) -> Subject:
    """Create a replay subject.

    A ReplaySubject is similar to a BehaviorSubject in that it can send
    old values to new subscribers, but it can also record a part
    of the Observable execution.

    A ReplaySubject records multiple values from the Observable
    execution and replays them to new subscribers.
    When a replay occurs, completed and error events are also replayed.

    Args:
        buffer_size (int): buffer size, or #items which be replayed on subscription
        subject_handler (Optional[SubjectHandler]): optional suject handler callback

    Returns:
        (Subject): the subject

    Raise:
        (RuntimeError): if buffer_size <= 0

    """
    if buffer_size <= 0:
        raise RuntimeError("buffer_size must be greater than zero!")

    _queue: Deque = deque(maxlen=buffer_size)
    _has_completed = False
    _error = None
    _subject = subject(subject_handler=subject_handler)

    async def _on_next(item: Any) -> None:
        nonlocal _queue, _subject

        _queue.append(item)
        await _subject.on_next(item)

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _queue, _subject, _has_completed, _error

        subscription = await _subject.subscribe(an_observer)

        if _queue:
            for value in _queue:
                await an_observer.on_next(value)

        if _error:
            await an_observer.on_error(_error)
        elif _has_completed:
            await an_observer.on_completed()

        return subscription

    async def _on_complete():
        nonlocal _has_completed
        _has_completed = True
        await _subject.on_completed()

    async def _on_error(err: Any) -> Optional[NoReturn]:
        nonlocal _error
        _error = err
        await _subject.on_error(err=err)

    return SubjectDefinition(subscribe=_subscribe, on_next=_on_next, on_error=_on_error, on_completed=_on_complete)
