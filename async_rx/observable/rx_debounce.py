from typing import Any, Optional
from datetime import timedelta, datetime
import curio
from ..protocol import Observable, Subscription, Observer, rx_observer

__all__ = ["rx_debounce"]


def rx_debounce(an_observable: Observable, time_delta: timedelta) -> Observable:
    """Debounce operator.

    Debounce are used to rate-limit the sequence. 
    Debounce will delay a value when it arrives and only emits the last value in a burst of events
    after the set delay is over and no new event arrives during this delay.

    Args:
        observable (Observable): an observable instance
        time_delta (timedelta): timedelta of interval (the duration)

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        _lastest_value_time = None
        _lastest_value = None
        _consumer_task = None
        _subscription: Optional[Subscription] = None
        _duration = timedelta.total_seconds

        async def consumer():
            nonlocal _duration, _lastest_value, _lastest_value_time
            try:
                while True:
                    await curio.sleep(_duration)  # add duration delay before process a new one

                    if _lastest_value_time and (_lastest_value_time + time_delta <= datetime.utcnow()):  # no value between time delta
                        await an_observer.on_next(item=_lastest_value)

            except curio.TaskCancelled:
                # it's time to finish
                pass

        async def _on_next(item: Any):
            nonlocal _lastest_value, _lastest_value_time
            _lastest_value = item
            _lastest_value_time = datetime.utcnow()

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

        _subscription = await an_observable.subscribe(rx_observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed))

        return _subscribe

    return rx_create(subscribe=_subscribe, max_observer=1)
