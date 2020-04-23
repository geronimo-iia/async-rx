from ...protocol import Observable
from .rx_reduce import rx_reduce

__all__ = ["rx_min"]


def rx_min(observable: Observable) -> Observable:
    """Create an observable wich returns minimal item in the source when completes.

    Args:
        observable (observable): the observable source

    Returns:
        (Observable): observable instance

    """
    return rx_reduce(observable=observable, accumulator=lambda a, b: min(a, b) if a else b)
