from inspect import iscoroutinefunction
from typing import Any, Callable, Optional

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_create import rx_create

__all__ = ["rx_map"]


def rx_map(observable: Observable, transform: Callable, expand_kwarg_parameters: Optional[bool] = False) -> Observable:
    """Map operator.

    Map operator modifies an Observable<A> into Observable<B> given a function with the type A->B.

    For example, if we take the function x => 10 ∗ x and a list of 1,2,3. The result is 10,20,30, see figure 4.
    Note that this function did not change the type of the Observable but did change the values.

    Args:
        observable (Observable): an observable instance
        transform (Callable): transform function (sync or async)
        expand_kwarg_parameters (Optional[bool]): if true each item will be expanded as kwargs before call transform.

    Returns:
        (Observable): observable instance

    """

    _is_awaitable = iscoroutinefunction(transform)

    async def _subscribe(an_observer: Observer) -> Subscription:
        async def _on_next(item: Any):
            nonlocal _is_awaitable

            if expand_kwarg_parameters:
                _next_item = await transform(**item) if _is_awaitable else transform(**item)
            else:
                _next_item = await transform(item) if _is_awaitable else transform(item)

            await an_observer.on_next(item=_next_item)

        return await observable.subscribe(rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe)
