from typing import Any, Optional

import curio

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
            (duration, value) = item
            await curio.sleep(duration * ratio)
            await an_observer.on_next(item=value)

        async def _producer():
            nonlocal _task
            try:
                if hasattr(source, "__aiter__"):
                    async for item in source:
                        await _proceed_item(item=item)
                else:
                    for item in source:
                        await _proceed_item(item=item)

                _task = None  # do not cancel this task if concurrent call to _subscribe occurs
                await an_observer.on_completed()
            except curio.TaskCancelled:  # pragma: no cover
                # it's time to finish
                pass

        _task = await curio.spawn(_producer())

        async def _subscribe():
            nonlocal _task
            if _task:  # pragma: no cover
                await _task.cancel()

        return _subscribe

    return rx_create(subscribe=_subscribe)
