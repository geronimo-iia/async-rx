from typing import Any

from ..protocol import Observable, Observer, Subscription, default_subscription
from .rx_create import rx_create

__all__ = ["rx_throw"]


def rx_throw(error: Any) -> Observable:
    """Create an observable wich always call error.

    Args:
        error (Union[Any, Exception]): the error to observe

    Returns:
        (Observable): observable instance.

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_error(err=error)

        return default_subscription

    return rx_create(subscribe=_subscribe)
