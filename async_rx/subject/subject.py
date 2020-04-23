from typing import Any, Optional, Union

from ..observer import ensure_observable_contract_operator, observer
from ..protocol import Observer, Subject, SubjectDefinition, SubjectHandler, Subscription

__all__ = ["subject"]


def subject(subject_handler: Optional[SubjectHandler] = None) -> Subject:
    """Create a subject.

    A Subject is like an Observable, but can multicast to many Observers.
    Subjects are like EventEmitters: they maintain a registry of many listeners,
    and then dispatch events/items to them.

    As subject is also an Observer, it can subscribe to an observable which act at his stream data source.

    Args:
        subject_handler (Optional[SubjectHandler]): optional suject handler callback

    Returns:
        (Subject): the subject

    TODO: check with curio how to wait on array of awaitable: With TaskGroup user in a context manager.

    """
    _registry = []  # list of registered observer

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _registry

        _registry.append(an_observer)

        if subject_handler:
            await subject_handler.on_subscribe(count=len(_registry), source=an_observer)

        async def unsubscribe() -> None:
            nonlocal _registry

            _registry.remove(an_observer)

            if subject_handler:
                await subject_handler.on_unsubscribe(count=len(_registry), source=an_observer)

        return unsubscribe

    async def _on_next(item: Any) -> None:
        nonlocal _registry

        for o in _registry:
            await o.on_next(item=item)

    async def _on_error(err: Union[Any, Exception]) -> None:
        nonlocal _registry

        for o in _registry:
            try:
                await o.on_error(err=err)
            except Exception:
                pass

    async def _on_completed() -> None:
        nonlocal _registry

        for o in _registry:
            await o.on_completed()

    _obs = ensure_observable_contract_operator(observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed))

    return SubjectDefinition(subscribe=_subscribe, on_next=_obs.on_next, on_error=_obs.on_error, on_completed=_obs.on_completed)
