from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_buffer import rx_buffer
from .rx_create import rx_create
from .rx_from import rx_from

__all__ = ["rx_window"]


def rx_window(observable: Observable, buffer_size: int) -> Observable:
    """Window operator.

    Window collect elements from the source sequence and emit them in groups.
    Window emits these elements in nested observables.
    It will emit a new inner observable when a window opens and will complete the inner observable when the window closes.
    Notice that there can be overlap between multiple windows if the next one opens before the last one closes.

    For example Window with a count of 2 and a skip of 1 will emit the last 2 elements (count 2) for every element (skip 1),
    so the sequence -1-2-3-4-| becomes --[12][23][34][4]|.

    Args:
        observable (Observable): the source
        buffer_size (int): buffer size

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if buffer_size <= 0

    """
    _buffer = rx_buffer(observable=observable, buffer_size=buffer_size)

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _buffer

        async def _on_next(item: Any) -> None:
            await an_observer.on_next(item=rx_from(item))
            return None

        return observable.subscribe(rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe, max_observer=1)
