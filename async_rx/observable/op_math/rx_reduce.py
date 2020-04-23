from inspect import iscoroutinefunction
from typing import Any, Optional, TypeVar

from ...observer import observer
from ...protocol import AccumulatorOperator, Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_reduce"]

T = TypeVar('T')


def rx_reduce(observable: Observable, accumulator: AccumulatorOperator, seed: Optional[Any] = None) -> Observable:
    """Create an observable which reduce source with accumulator and seed value.

    Args:
        observable (Observable): source
        accumulator (AccumulatorOperator): accumulator function (two argument, one result) async or sync.
        seed (Optional[Any]): optional seed value (default none)

    Returns:
        (Observable): a new observable

    """

    is_awaitable = iscoroutinefunction(accumulator)

    async def _subscribe(an_observer: Observer) -> Subscription:
        nonlocal is_awaitable

        _buffer = seed

        async def _on_next(item: Any):
            nonlocal _buffer
            _buffer = await accumulator(_buffer, item) if is_awaitable else accumulator(_buffer, item)

        async def _on_completed():
            nonlocal _buffer

            await an_observer.on_next(item=_buffer)
            await an_observer.on_completed()

        return await observable.subscribe(an_observer=observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=_on_completed))

    return rx_create(subscribe=_subscribe)
