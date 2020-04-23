from ...protocol import Observable
from .rx_reduce import rx_reduce

__all__ = ["rx_sum"]


def rx_sum(observable: Observable) -> Observable:
    """Create an observable wich return the sum items in the source when completes.

    Args:
        observable (observable): the observable source

    Returns:
        (Observable): observable instance

    """
    return rx_reduce(observable=observable, accumulator=lambda current, inc: current + inc, seed=0)
