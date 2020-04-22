from collections import deque
from typing import Any, Deque

from ..observable import rx_create
from ..observer import observer
from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_last"]


def rx_last(observable: Observable, count: int = 1) -> Observable:
    """Create an observale which only take #count (or less) last events and complete.

    Args:
        observable (Observable): observable source
        count (int): number of event to get (default 1)

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if count <= 0

    """
    if count <= 0:
        raise RuntimeError('count must be greather than zero')

    async def _subscribe(an_observer: Observer) -> Subscription:
        # local buffer of #count
        _q: Deque = deque(maxlen=count)

        async def _on_next(item: Any):
            nonlocal _q

            _q.append(item)

        async def _on_completed():
            nonlocal _q

            for item in _q:
                await an_observer.on_next(item=item)
            _q.clear()
            await an_observer.on_completed()

        return await observable.subscribe(an_observer=observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=_on_completed))

    return rx_create(subscribe=_subscribe)
