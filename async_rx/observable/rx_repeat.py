from datetime import timedelta
from inspect import iscoroutinefunction
from typing import Callable

import curio

from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create

__all__ = ["rx_repeat"]


def rx_repeat(duration: timedelta, producer: Callable) -> Observable:
    """Repeat data.

    rx_repeat send data generated by producer function at duration rate until observer
    dispose his subscription.

    Args:
        duration (timedelta): duration between each sended item
        producer (Callable): producer (asyn/sync) function

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if no producer or duration are provided

    """
    if not producer or not duration:
        raise RuntimeError("producer and duration are mandatory")

    _is_awaitable = iscoroutinefunction(producer)
    _duration = duration.total_seconds()

    async def _subscribe(an_observer: Observer) -> Subscription:
        _task = None

        async def _producer():
            nonlocal _duration, _is_awaitable
            try:
                while True:
                    await curio.sleep(_duration)
                    value = await producer() if _is_awaitable else producer()
                    await an_observer.on_next(item=value)
            except curio.TaskCancelled:
                # it's time to finish
                pass

        _task = await curio.spawn(_producer())

        async def _subscribe():
            nonlocal _task
            if _task:
                await an_observer.on_completed()
                await _task.cancel()
                _task = None

        return _subscribe

    return rx_create(subscribe=_subscribe)
