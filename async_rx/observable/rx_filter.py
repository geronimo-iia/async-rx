from inspect import iscoroutinefunction
from typing import Any

from ..protocol import Observable, Observer, PredicateOperator, Subscription, rx_observer_from
from .rx_create import rx_create

__all__ = ["rx_filter"]


def rx_filter(observable: Observable, predicate: PredicateOperator) -> Observable:
    """Create an observable which event are filtered by a predicate function.

    Args:
        observable (Observable): observable source
        predicate (Operator): predicate function which take on argument and return
            a truthy value

    Returns:
        (Observable): observable instance

    """

    _awaitable = iscoroutinefunction(predicate)

    async def _subscribe(an_observer: Observer) -> Subscription:
        async def _on_next(item: Any):
            nonlocal _awaitable
            _test = await predicate(item) if _awaitable else predicate(item)  # type: ignore
            if _test:
                await an_observer.on_next(item)

        return await observable.subscribe(an_observer=rx_observer_from(observer=an_observer, on_next=_on_next))

    return rx_create(subscribe=_subscribe)
