from typing import Any, List, NoReturn, Optional

import curio

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_merge"]


def rx_merge(*observables: Observable) -> Observable:
    """Flattens multiple Observables together by blending their values into one Observable.

    Creates an output Observable which concurrently emits all values
    from every given input Observable.
    'merge' subscribes to each given input Observable (either the source or
    an Observable given as argument), and simply forwards (without doing any
    transformation) all the values from all the input Observables to the output
    Observable.
    The output Observable only completes once all input Observables have completed.
    Any error delivered by an input Observable will be immediately emitted on
    the output Observable.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if #observables < 1

    """
    if len(observables) < 1:
        raise RuntimeError("#observables must be greather than 1")

    terminated_observable = 0
    deliver_next = True
    subscriptions: List[Subscription] = []

    async def _subscription_handler() -> None:
        nonlocal subscriptions
        for s in subscriptions:
            await s()

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal subscriptions

        async def _on_next(item: Any) -> None:
            # filter item according to deliver_next
            nonlocal deliver_next

            if deliver_next:  # if no previous error
                await an_observer.on_next(item)
            return None

        async def _on_completed() -> None:
            nonlocal terminated_observable, deliver_next

            if deliver_next:  # if no previous error
                terminated_observable += 1
                if terminated_observable == len(observables):  # and all observable complete
                    # lock on_next, on_error handler call and other on_completed call.
                    deliver_next = False
                    await an_observer.on_completed()
            return None

        async def _on_error(err: Any) -> Optional[NoReturn]:
            nonlocal deliver_next

            if deliver_next:
                # lock on_next, on_completed handler call and other on_error call.
                deliver_next = False
                await an_observer.on_error(err)
            return None

        # local observer definition
        _observer = rx_observer(on_next=_on_next, on_completed=_on_completed, on_error=_on_error)

        # local observer subscribe to all observables in parallele
        _tasks = []
        async with curio.TaskGroup(wait=all) as g:
            for an_observable in observables:
                _tasks.append(await g.spawn(an_observable.subscribe, _observer))
        subscriptions = [t.result for t in _tasks]

        return _subscription_handler

    return rx_create(subscribe=_subscribe, max_observer=1)
