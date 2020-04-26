from typing import Any

from ..protocol import Observable, Observer, PredicateOperator, Subscription, rx_observer
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

    async def _subscribe(an_observer: Observer) -> Subscription:
        async def _on_next(item: Any):
            if await predicate(item=item):
                await an_observer.on_next(item=item)

        return await observable.subscribe(an_observer=rx_observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=an_observer.on_completed))

    return rx_create(subscribe=_subscribe)
