from datetime import datetime, timedelta
from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_create import rx_create

__all__ = ["rx_throttle"]


def rx_throttle(observable: Observable, duration: timedelta) -> Observable:
    """Throttle operator.

    Throttle are used to rate-limit the sequence.
    They will filter out elements based on the timing.

    Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout

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

        _last_send_item = None

        async def _on_next(item: Any):
            nonlocal _last_send_item
            _now = datetime.utcnow()
            if not _last_send_item or _last_send_item + duration <= _now:
                _last_send_item = _now
                await an_observer.on_next(item)

        return await observable.subscribe(rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe, max_observer=1)
