from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create
from .rx_reduce import rx_reduce

__all__ = ["rx_avg"]


def rx_avg(observable: Observable) -> Observable:
    """Create an observable wich return the average items in the source when completes.

    Args:
        observable (observable): the observable source

    Returns:
        (Observable): observable instance

    """

    _count = 0

    async def accumulator(current, item):
        nonlocal _count
        _count += 1
        return current + item

    async def _subscribe(an_observer: Observer) -> Subscription:

        reducer = rx_reduce(observable=observable, accumulator=accumulator, seed=0)

        async def _on_next(item: Any):
            nonlocal _count
            if _count == 0:
                await an_observer.on_error('No value emitted')
            else:
                await an_observer.on_next(item=item / _count)

        return await reducer.subscribe(an_observer=rx_observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=an_observer.on_completed))

    return rx_create(subscribe=_subscribe)
