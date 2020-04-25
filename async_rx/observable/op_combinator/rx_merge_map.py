from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_merge_map"]


def rx_merge_map(*observables: Observable) -> Observable:
    """Merge map operator.

    rx_merge_map allows asynchronous queries, resulting in an observable of observables and it flattens the results.
    There may be multiple inner observables that run simultaneously, so the results from these inner observables may be intertwined.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
