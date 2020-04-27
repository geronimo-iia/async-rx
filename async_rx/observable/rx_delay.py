from datetime import timedelta
from typing import Any, Optional

import curio

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_delay"]


def rx_delay(observable: Observable, duration: timedelta, buffer_size: Optional[int] = None, ignore_events_if_full: Optional[bool] = True) -> Observable:
    """Delay operator.

    Delay will project the sequence unmodified, but shifted into the future with a specified
    delay.

    Underlaying implementation use a queue and a dedicated consumer.

    Args:
        observable (Observable): an observable instance
        duration (timedelta): timedelta of delay (the duration).
        buffer_size (Optional[int]): optional buffer size, if not specified size is unlimited
            (ignore_events_if_full has no meaning, but not your memory...)
        ignore_events_if_full (Optional[bool]): When true, if internal buffer (here a queue) is full,
            events will be ignored until older will be consumed.
            Otherwise, producer will be locked until older will be consumed.

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        _queue = curio.Queue(buffer_size) if buffer_size else curio.Queue()
        _consumer_task = None
        _subscription: Optional[Subscription] = None
        _duration = timedelta.total_seconds

        async def consumer():
            nonlocal _queue, _duration
            try:
                while True:
                    item = await _queue.get()  # retreaive an item (lock until one)
                    await an_observer.on_next(item=item)
                    await _queue.task_done()  # notify that job is done
                    await curio.sleep(_duration)  # add duration delay before process a new one
            except curio.TaskCancelled:
                # it's time to finish
                pass

        async def _cancel_consumer():
            nonlocal _consumer_task
            if _consumer_task:
                await _consumer_task.cancel()
                _consumer_task = None

        async def _on_next(item: Any):
            nonlocal _queue
            if ignore_events_if_full and _queue.full():
                return
            await _queue.put(item)

        async def _on_completed():
            nonlocal _queue, _consumer_task
            await _queue.join()  # wait complete processing
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
