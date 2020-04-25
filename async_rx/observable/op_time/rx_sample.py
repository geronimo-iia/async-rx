from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_sample"]


def rx_sample(*observables: Observable) -> Observable:
    """Sample operator.

    The following three operators, Debounce, Sample and Throttle are used to rate-limit the sequence.
    They will filter out elements based on the timing. There is a difference in how they exactly do that.
    Debounce will delay a value when it arrives and only emits the last value in a burst of events
    after the set delay is over and no new event arrives during this delay. 
    Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout.
    Sample will emit the latest value on a set interval or emit nothing if no new value arrived during the last interval.


    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
