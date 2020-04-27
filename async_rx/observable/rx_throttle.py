from datetime import datetime, timedelta
from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_create import rx_create

__all__ = ["rx_throttle"]


def rx_throttle(observable: Observable, time_delta: timedelta) -> Observable:
    """Throttle operator.

    Throttle are used to rate-limit the sequence.
    They will filter out elements based on the timing.

    Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout

    Args:
        observable (Observable): an observable instance
        time_delta (timedelta): timedelta of interval (the duration)

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        _last_send_item = None

        async def _on_next(item: Any):
            nonlocal _last_send_item
            _now = datetime.utcnow()
            if not _last_send_item or _last_send_item + time_delta <= _now:
                _last_send_item = _now
                await an_observer.on_next(item=item)

        return await observable.subscribe(rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe, max_observer=1)
