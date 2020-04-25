import curio
from typing import List, Any, Optional, NoReturn
from ...protocol import Observable, Observer, Subscription, subscription_autocancel
from ..rx_create import rx_create
from ..op_filter import rx_first
from ...subject import subject
from ...observer import observer

__all__ = ["rx_amb"]


def rx_amb(*observables: Observable) -> Observable:
    """Amb operator.

    The Amb operator (stands for ambiguous), alias race, subscribes to a number of observables
    and retrieves the first observable that yields a value, closing off all others.
    For example, Amb can automatically select the best server to download from: Amb listens to both servers
    and the first server that replies is used.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if #observables < 1

    """

    if len(observables) < 1:
        raise RuntimeError("#observables must be greather than 1")

    async def _subscribe(an_observer: Observer) -> Subscription:

        _subject = subject()

        # we send the first
        _first_subscription: Subscription = rx_first(observable=_subject).subscribe(an_observer)

        # subscribe to all observables in parallele
        _subscriptions: List[Subscription] = []
        async with curio.TaskGroup(wait=all) as g:
            for an_observable in observables:
                _task = await g.spawn(_build_observer_and_subscribe, an_observable, _subject)
                _subscriptions.append(_task.result)

        async def _subscription_handler():
            nonlocal _first_subscription, _subscriptions
            if _first_subscription:
                await _first_subscription()
            for _unsub in _subscriptions:
                if _unsub:
                    await _unsub

        return _subscription_handler

    return rx_create(subscribe=_subscribe, max_observer=1)


async def _build_observer_and_subscribe(an_observable: Observable, an_observer: Observer):
    _observer = await _observer_for(an_observable=an_observable, an_observer=an_observer)
    return subscription_autocancel(an_observable=an_observable, an_observer=_observer)


async def _observer_for(an_observable: Observable, an_observer: Observer):
    """Build an observer that send observable when respond."""

    async def _on_next(item: Any) -> None:
        await an_observer.on_next(item=an_observable)
        return None

    async def _on_completed() -> None:
        await an_observer.on_next(item=an_observable)
        await an_observer.on_completed()
        return None

    async def _on_error(err: Any) -> Optional[NoReturn]:
        return None

    return observer(on_next=_on_next, on_completed=_on_completed, on_error=_on_error)
