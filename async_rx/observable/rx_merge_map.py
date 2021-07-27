from inspect import iscoroutinefunction
from typing import Any, Callable

from ..protocol import Observable, Observer, Subscription, rx_observer_from
from .rx_create import rx_create
from .rx_merge import rx_merge

__all__ = ["rx_merge_map"]


def rx_merge_map(*observables: Observable, transform: Callable) -> Observable:
    """Merge map operator.

    rx_merge_map allows asynchronous queries, resulting in an observable of observables and it flattens the results.
    There may be multiple inner observables that run simultaneously, so the results from these inner observables may be intertwined.

    Args:
        observables (Observable): a list of observable instance
        transform (Callable): transform function (sync or async)

    Returns:
        (Observable): observable instance

    """

    _is_awaitable = iscoroutinefunction(transform)
    _source = rx_merge(*observables)

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal _source

        async def _on_next(item: Any):
            nonlocal _is_awaitable
            if _is_awaitable:
                await an_observer.on_next(await transform(item))
            else:
                await an_observer.on_next(transform(item))

        return await _source.subscribe(rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe, max_observer=1)
