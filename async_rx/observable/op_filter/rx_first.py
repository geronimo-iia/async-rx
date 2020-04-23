from ...protocol import Observable
from .rx_take import rx_take

__all__ = ["rx_first"]


def rx_first(observable: Observable) -> Observable:
    """Create an observale which only take the first event and complete.

    Args:
        observable (Observable): observable source

    Returns:
        (Observable): observable instance

    """
    return rx_take(observable=observable, count=1)
