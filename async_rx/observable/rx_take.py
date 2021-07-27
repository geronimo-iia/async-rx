from typing import Any, Optional

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_create import rx_create

__all__ = ["rx_take"]


def rx_take(observable: Observable, count: int) -> Observable:
    """Create an observable which take only first #count event maximum (could be less).

    Args:
        observable (Observable): observable source
        count (int): #items to take

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if count <= 0

    """
    if count <= 0:
        raise RuntimeError('count must be greather than zero')

    async def _subscribe(an_observer: Observer) -> Subscription:

        _count: int = 0
        _subscription: Optional[Subscription] = None

        async def _unsubscribe():
            nonlocal _subscription

            if _subscription:
                await _subscription()
                _subscription = None

        async def _on_next(item: Any):
            nonlocal _count, _subscription

            if _count < count:
                _count += 1
                await an_observer.on_next(item)

            if _count == count:
                await an_observer.on_completed()

        _subscription = await observable.subscribe(an_observer=rx_observer_from(observer=an_observer, on_next=_on_next))

        return _unsubscribe

    return rx_create(subscribe=_subscribe)
