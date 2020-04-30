from datetime import timedelta
from typing import Any, Optional

import curio

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_sample"]


def rx_sample(observable: Observable, duration: timedelta) -> Observable:
    """Sample operator used to rate-limit the sequence.

    Sample filter out elements based on the timing.
    Sample will emit the LATEST value on a set interval or emit nothing if no new value arrived during the last interval.


    Args:
        observable (Observable): an observable instance
        duration (timedelta): timedelta of interval (the duration)

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if no observable or duration are provided

    """
    if not observable or not duration:
        raise RuntimeError("observable and duration are mandatory")

    async def _subscribe(an_observer: Observer) -> Subscription:

        _receive_value = False
        _lastest_value = None
        _consumer_task = None
        _subscription: Optional[Subscription] = None
        _duration = duration.total_seconds()

        async def consumer():
            nonlocal _duration, _lastest_value, _receive_value
            try:
                while True:
                    await curio.sleep(_duration)  # add duration delay before process a new one
                    if _receive_value:
                        await an_observer.on_next(item=_lastest_value)
                        _receive_value = False

            except curio.TaskCancelled:
                # it's time to finish
                pass

        async def _on_next(item: Any):
            nonlocal _lastest_value, _receive_value
            _lastest_value = item
            _receive_value = True

        async def _cancel_consumer():
            nonlocal _consumer_task
            if _consumer_task:
                await _consumer_task.cancel()
                _consumer_task = None

        async def _on_completed():
            nonlocal _consumer_task
            await _cancel_consumer()
            await an_observer.on_completed()

        async def _on_error(err: Any):
            nonlocal _consumer_task
            await _cancel_consumer()
            await an_observer.on_error(err=err)

        async def _subscribe():
            nonlocal _consumer_task, _subscription
            await _cancel_consumer()
            if _subscription:
                await _subscription()
                _subscription = None

        _consumer_task = await curio.spawn(consumer())

        _subscription = await observable.subscribe(rx_observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed))

        return _subscribe

    return rx_create(subscribe=_subscribe, max_observer=1)
