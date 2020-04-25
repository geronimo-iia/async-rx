from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_map"]


def rx_map(*observables: Observable) -> Observable:
    """Map operator.

    Map operator modifies an Observable<A> into Observable<B> given a function with the type A->B.
    
    For example, if we take the function x => 10 ∗ x and a list of 1,2,3. The result is 10,20,30, see figure 4.
    Note that this function did not change the type of the Observable but did change the values.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
