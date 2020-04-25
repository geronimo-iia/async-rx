from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_delay"]


def rx_delay(*observables: Observable) -> Observable:
    """Delay operator.

    Delay will project the sequence unmodified, but shifted into the future with a specified
    delay.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
