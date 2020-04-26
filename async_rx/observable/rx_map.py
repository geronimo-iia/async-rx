from inspect import iscoroutinefunction
from typing import Callable, Any
from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_map"]


def rx_map(observable: Observable, transform: Callable) -> Observable:
    """Map operator.

    Map operator modifies an Observable<A> into Observable<B> given a function with the type A->B.

    For example, if we take the function x => 10 ∗ x and a list of 1,2,3. The result is 10,20,30, see figure 4.
    Note that this function did not change the type of the Observable but did change the values.

    Args:
        observable (Observable): an observable instance
        transform (Callable): transform function (sync or async)

    Returns:
        (Observable): observable instance

    """

    _is_awaitable = iscoroutinefunction(transform)

    async def _subscribe(an_observer: Observer) -> Subscription:
        async def _on_next(item: Any):
            nonlocal _is_awaitable
            if _is_awaitable:
                await an_observer.on_next(item=await transform(item))
            else:
                await an_observer.on_next(item=transform(item))

        return await observable.subscribe(rx_observer(on_next=_on_next, on_completed=an_observer.on_completed, on_error=an_observer.on_error))

    return rx_create(subscribe=_subscribe)
