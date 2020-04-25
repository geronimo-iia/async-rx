from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_throttle"]


def rx_throttle(*observables: Observable) -> Observable:
    """Throttle operator.

    Throttle are used to rate-limit the sequence.
    They will filter out elements based on the timing. 

    Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
