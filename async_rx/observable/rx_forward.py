from typing import Any

from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create

__all__ = ["rx_forward"]


def rx_forward(observable: Observable, except_complet: bool = False, except_error: bool = False) -> Observable:
    """Create an observable wich forward event.

    Args:
        observable (Observable): observable source
        except_complet (bool): if true then did not forward 'on_complet' (default: {False})
        except_error (bool): if true then did not forward 'on_error' (default: {False})

    Returns:
        (Observable): observable instance.

    """

    async def _dummy_on_completed():
        pass

    async def _dummy_on_error(err: Any):
        pass

    async def _subscribe(an_observer: Observer) -> Subscription:

        return await observable.subscribe(
            an_observer=rx_observer(
                on_next=an_observer.on_next,
                on_error=_dummy_on_error if except_error else an_observer.on_error,
                on_completed=_dummy_on_completed if except_complet else an_observer.on_completed,
            )
        )

    return rx_create(subscribe=_subscribe)
