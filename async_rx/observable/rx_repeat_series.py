import curio
from typing import Optional, Any
from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create

__all__ = ["rx_repeat_series"]


def rx_repeat_series(source: Any, ratio: Optional[float] = 1.0) -> Observable:
    """Repeat a series (delay, value) as an observable for each subscription.

    Args:
        source (Any): iterable or async iterable source of tuple (duration, value)
        ratio (Optional[float]): ratio apply on duration (1.0 per default)

    Returns:
        (Observable): an observable

    Raise:
        (RuntimeError): if source is not iterable (sync or async)

    """
    if not hasattr(source, "__iter__") and not hasattr(source, "__aiter__"):
        raise RuntimeError("source must be (async/sync) iterable")

    async def _subscribe(an_observer: Observer) -> Subscription:
        _task = None

        async def _proceed_item(item: Any):
            nonlocal an_observer
            (duration, value) = item
            await curio.sleep(duration * ratio)
            await an_observer.on_next(item=value)

        async def _producer():
            nonlocal an_observer, _task
            try:
                if hasattr(source, "__aiter__"):
                    async for item in source:
                        await _proceed_item(item=item)
                else:
                    for item in source:
                        await _proceed_item(item=item)
                await an_observer.on_completed()
            except curio.TaskCancelled:
                # it's time to finish
                _task = None

        _task = await curio.spawn(_producer())

        async def _subscribe():
            nonlocal _task
            if _task:
                await _task.cancel()

        return _subscribe

    return rx_create(subscribe=_subscribe)
