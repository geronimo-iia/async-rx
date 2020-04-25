"""Subscription utilities."""
import curio
from typing import Optional
from .definition import Observable, Observer, Subscription

__all__ = ["default_subscription", "disposable_subscription_on_cancel"]


async def default_subscription() -> None:
    """Default subcribe implementation method.

    Do nothing.

    Returns:
        (None) - nothing to return.

    """
    pass


async def disposable_subscription_on_cancel(an_observable: Observable, an_observer: Observer) -> Optional[Subscription]:
    """Subscribe implementation wich dispose herself on cancel.

    Arguments:
        an_observable (Observable): observable
        an_observer (Observer): observer

    Returns:
        (Optional[Subscription]): the subscription if task is not cancelled

    """
    _subscription: Optional[Subscription] = None
    try:
        _subscription = await an_observable.subscribe(an_observer=an_observer)
    except curio.CancelledError:
        if _subscription:
            await _subscription()
            _subscription = None
    return _subscription
