from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create
from .subscription import default_subscription

__all__ = ["rx_range"]


def rx_range(start: int, stop: int, step: int = 1) -> Observable:
    """Create an observable sequence of range.

    Args:
        start (int): initiale value
        stop (int): last value
        step (int): default increment (default: {1})

    Returns:
        (Observable): observable instance.

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        for i in range(start=start, stop=stop, step=step):
            await an_observer.on_next(item=i)
        await an_observer.on_completed()

        return default_subscription

    return rx_create(subscribe=_subscribe)
