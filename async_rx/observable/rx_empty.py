from ..protocol import Observable, Observer, Subscription
from .rx_create import rx_create
from .subscription import default_subscription

__all__ = ["rx_empty"]


def rx_empty() -> Observable:
    """Create an empty Observable.

    An "empty" Observable emits only the complete notification.

    Returns:
        (Observable) observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_completed()
        return default_subscription

    return rx_create(subscribe=_subscribe)
