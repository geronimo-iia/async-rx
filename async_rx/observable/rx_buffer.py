from collections import deque
from typing import Any, Deque, Optional

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_buffer"]


def rx_buffer(observable: Observable, buffer_size: int) -> Observable:
    """Buffer operator.

    Buffer and Window collect elements from the source sequence and emit them in groups.
    Buffer projects these elements onto list and emits them, start to process source on first subscription.

    Args:
        observable (Observable): the source
        buffer_size (int): buffer size

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if buffer_size <= 0

    """

    if buffer_size <= 0:
        raise RuntimeError('count must be greather than zero')

    async def _subscribe(an_observer: Observer) -> Subscription:
        _queue: Deque = deque(maxlen=buffer_size)
        _unsub: Optional[Subscription] = None

        async def flush():
            nonlocal _queue
            if len(_queue) >= buffer_size:
                await an_observer.on_next(list(_queue))
                _queue.clear()

        async def _on_next(item: Any) -> None:
            nonlocal _queue
            _queue.append(item)
            await flush()
            return None

        async def _on_completed() -> None:
            nonlocal _queue
            await flush()
            await an_observer.on_completed()
            return None

        async def _on_error(err: Any) -> None:
            await flush()
            await an_observer.on_error(err=err)
            return None

        async def _unsubscribe():
            nonlocal _queue
            _queue.clear()
            if _unsub:
                await _unsub()

        _unsub = await observable.subscribe(rx_observer(on_next=_on_next, on_completed=_on_completed, on_error=_on_error))

        return _unsubscribe

    return rx_create(subscribe=_subscribe, max_observer=1)
