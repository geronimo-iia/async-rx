from ..protocol import Observable
from .rx_reduce import rx_reduce

__all__ = ["rx_count"]


def rx_count(observable: Observable) -> Observable:
    """Create an observable wich counts the emissions on the source and emits result.

    Args:
        observable (observable): the observable source

    Returns:
        (Observable): observable instance

    """
    return rx_reduce(observable=observable, accumulator=lambda emit, item: emit + 1, seed=0)
