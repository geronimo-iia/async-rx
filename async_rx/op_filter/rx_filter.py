from typing import Any, Protocol

from ..observable import rx_create
from ..observer import observer
from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_filter", "BooleanOperator"]


class BooleanOperator(Protocol):
    """BooleanOperator Protocol."""

    async def __call__(self, item: Any) -> bool:
        pass


def rx_filter(observable: Observable, predicate: BooleanOperator) -> Observable:
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

        return await observable.subscribe(an_observer=observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=an_observer.on_completed))

    return rx_create(subscribe=_subscribe)
