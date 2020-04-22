from typing import Any, Optional, Protocol, TypeVar, Union

from ..observable import rx_create
from ..observer import observer
from ..protocol import Observable, Observer, Subscription

__all__ = ["Accumulator", "rx_reduce"]

T = TypeVar('T')


class AsyncAccumulator(Protocol[T]):
    async def __call__(self, buffer: T, item: T) -> T:
        pass


class SyncAccumulator(Protocol[T]):
    def __call__(self, buffer: T, item: T) -> T:
        pass


Accumulator = Union[AsyncAccumulator, SyncAccumulator]


def rx_reduce(observable: Observable, accumulator: Accumulator, seed: Optional[Any] = None) -> Observable:
    """Create an observable which reduce source with accumulator and seed value.

    Args:
        observable (Observable): source
        accumulator (Union[Callable[[Any, Any], Awaitable[Any]], Callable[[Any, Any], Any]]):  # noqa: E501
            accumulator function (two argument, one result) async or sync.
        seed (Optional[Any]): optional seed value (default none)

    Returns:
        (Observable): a new observable

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        _buffer = seed

        async def _on_next(item: Any):
            nonlocal _buffer

            _buffer = await accumulator(buffer=_buffer, item=item)

        async def _on_completed():
            nonlocal _buffer

            await an_observer.on_next(item=_buffer)
            await an_observer.on_completed()

        return await observable.subscribe(an_observer=observer(on_next=_on_next, on_error=an_observer.on_error, on_completed=_on_completed))

    return rx_create(subscribe=_subscribe)
