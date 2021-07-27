from typing import Any, Dict

from ..protocol import Observable, Observer, Subscription, default_subscription
from .rx_create import rx_create
from .rx_dict import rx_dict

__all__ = ["rx_from"]


def rx_from(observable_input: Any) -> Observable:
    """Convert almost anything to an Observable.

    Anything means:
        - a dictionnary in an rx_dict
        - an async iterable
        - an iterable
        - something which can be cast to an Observable (have a subscribe function)
        - an object

    Args:
        observable_input (Any): A subscribable object

    Returns:
        (Observable): The Observable whose values are originally from the input object
            that was converted.

    """
    if isinstance(observable_input, Dict):
        return rx_dict(initial_value=observable_input)

    if hasattr(observable_input, "subscribe"):
        # observable like
        return rx_create(subscribe=observable_input.subscribe)

    if hasattr(observable_input, "__aiter__"):
        # something which be async iterable
        async def _subscribe_aiter(an_observer: Observer) -> Subscription:
            async for item in observable_input:
                await an_observer.on_next(item)
            await an_observer.on_completed()

            return default_subscription

        return rx_create(subscribe=_subscribe_aiter)

    if hasattr(observable_input, "__iter__"):
        # something iterable
        async def _subscribe_iter(an_observer: Observer) -> Subscription:
            for item in observable_input:
                await an_observer.on_next(item)
            await an_observer.on_completed()

            return default_subscription

        return rx_create(subscribe=_subscribe_iter)

    # Build an simple singleton

    async def _subscribe_object(an_observer: Observer) -> Subscription:
        await an_observer.on_next(observable_input)
        await an_observer.on_completed()

        return default_subscription

    return rx_create(subscribe=_subscribe_object)
