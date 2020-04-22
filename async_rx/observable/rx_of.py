from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create
from .subscription import default_subscription

__all__ = ["rx_of"]


def rx_of(*args) -> Observable:
    """Convert arguments into an observable sequence.

    Args:
        args: any list of argument to send to observer.

    Returns:
        (Observable): observable instance.

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        for arg in args:
            await an_observer.on_next(item=arg)
        await an_observer.on_completed()

        return default_subscription

    return rx_create(subscribe=_subscribe)
