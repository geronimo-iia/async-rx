from typing import Any

from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create
from .subscription import default_subscription

__all__ = ["rx_from"]


def rx_from(observable_input: Any) -> Observable:
    """Convert almost anything to an Observable.

    Args:
        observable_input (Any): A subscribable object

    Returns:
        (Observable): The Observable whose values are originally from the input object
            that was converted.

    """
    if hasattr(observable_input, "subscribe"):
        # observable like
        return rx_create(subscribe=observable_input.subscribe)

    if hasattr(observable_input, "__aiter__"):
        # something which be async iterable
        async def _subscribe_aiter(an_observer: Observer) -> Subscription:
            async for item in observable_input:
                await an_observer.on_next(item=item)
            await an_observer.on_completed()

            return default_subscription

        return rx_create(subscribe=_subscribe_aiter)

    if hasattr(observable_input, "__iter__"):
        # something iterable
        async def _subscribe_iter(an_observer: Observer) -> Subscription:
            for item in observable_input:
                await an_observer.on_next(item=item)
            await an_observer.on_completed()

            return default_subscription

        return rx_create(subscribe=_subscribe_iter)

    # Build an simple singleton

    async def _subscribe_object(an_observer: Observer) -> Subscription:
        await an_observer.on_next(item=_subscribe_object)
        await an_observer.on_completed()

        return default_subscription

    return rx_create(subscribe=_subscribe_object)
