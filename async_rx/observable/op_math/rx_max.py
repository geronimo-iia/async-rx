from ...protocol import Observable
from .rx_reduce import rx_reduce

__all__ = ["rx_max"]


def rx_max(observable: Observable) -> Observable:
    """Create an observable wich returns the maximal item in the source when completes.

    Args:
        observable (observable): the observable source

    Returns:
        (Observable): observable instance

    """
    return rx_reduce(observable=observable, accumulator=lambda a, b: max(a, b) if a else b)
