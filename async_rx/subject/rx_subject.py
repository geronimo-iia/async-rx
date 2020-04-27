from typing import Any, Optional, Union

from ..protocol import Observer, Subject, SubjectHandler, Subscription, ensure_observable_contract_operator, rx_observer, subject

__all__ = ["rx_subject"]


def rx_subject(subject_handler: Optional[SubjectHandler] = None) -> Subject:
    """Create a subject.

    A Subject is like an Observable, but can multicast to many Observers.
    Subjects are like EventEmitters: they maintain a registry of many listeners,
    and then dispatch events/items to them.

    As subject is also an Observer, it can subscribe to an observable which act at his stream data source.

    Args:
        subject_handler (Optional[SubjectHandler]): optional suject handler callback

    Returns:
        (Subject): the subject

    Example 1:

    .. highlight:: python
    .. code-block:: python

        # create a subject
        a_subject = subject(subject_handler=my_handler)

        # few observer subscribe on this subject
        sub_1 = await a_subject.subscribe(obs_1)
        sub_2 = await a_subject.subscribe(obs_2)

        # the subject subscribe himself on an observable
        await rx_range(start=0, stop=10).subscribe(a_subject)

        # obs_1 and obs_2 receive 10 #items

    Example 2:
    A subject as event emitter

    .. highlight:: python
    .. code-block:: python

        # create a subject
        a_subject = subject()

        # few observer subscribe on this subject
        sub_1 = await a_subject.subscribe(obs_1)
        sub_2 = await a_subject.subscribe(obs_2)

        # send your data by your self
        await a_subject.on_next(item="my value") # obs_1 and obs_2 receive "my value"
        await a_subject.on_completed() # obs_1 and obs_2 receive on_completed


    """
    _registry = []  # list of registered observer

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _registry

        _registry.append(an_observer)

        if subject_handler:
            await subject_handler.on_subscribe(count=len(_registry), source=an_observer)

        async def unsubscribe() -> None:
            nonlocal _registry
            if an_observer in _registry:
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
            except Exception:  # pragma: no cover
                pass

    async def _on_completed() -> None:
        nonlocal _registry

        for o in _registry:
            await o.on_completed()

    _obs = ensure_observable_contract_operator(rx_observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed))

    return subject(subscribe=_subscribe, on_next=_obs.on_next, on_error=_obs.on_error, on_completed=_obs.on_completed)
