from collections import deque
from typing import Any, Deque

from ..observable import rx_create
from ..observer import observer
from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_distinct"]


def rx_distinct(observable: Observable, frame_size: int) -> Observable:
    """Create an observable which send distinct event inside a windows of size #frame_size.

    Args:
        observable (Observable): observable source
        frame_size (int): windows size

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if frame_size <= 0

    """
    if frame_size <= 0:
        raise RuntimeError('framesize must be greather than zero')

    async def _subscribe(an_observer: Observer) -> Subscription:

        # our frame buffer
        _q: Deque = deque(maxlen=frame_size)

        async def _on_next(item: Any):
            nonlocal _q

            if item not in _q:  # distinct value
                _q.append(item)
                await an_observer.on_next(item=item)

        async def _on_completed():
            nonlocal _q

            _q.clear()
            await an_observer.on_completed()

        return await observable.subscribe(an_observer=observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=_on_completed))

    return rx_create(subscribe=_subscribe)
