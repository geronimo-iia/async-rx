from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_skip"]


def rx_skip(observable: Observable, count: int) -> Observable:
    """Create an obervable wich skip #count event on source.

    Args:
        observable (Observable): observable source
        count (int): number of event to skip

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if count <= 0

    """
    if count <= 0:
        raise RuntimeError('count must be greather than zero')

    async def _subscribe(an_observer: Observer) -> Subscription:

        _count: int = 0

        async def _on_next(item: Any):
            nonlocal _count

            if _count < count:
                _count += 1
            else:
                await an_observer.on_next(item=item)

        return await observable.subscribe(an_observer=rx_observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=an_observer.on_completed))

    return rx_create(subscribe=_subscribe)
