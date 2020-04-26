from ..protocol import Observable, Observer, Subscription, rx_observer
from .rx_create import rx_create
from typing import Optional, Any

__all__ = ["rx_concat"]


def rx_concat(*observables: Observable) -> Observable:
    """Concat operator.

    Merge and Concat combine multiple sequences into one.
    Merge might interweave elements from different sequence
    whereas Concat emits all elements from the first sequence before turning to the next one.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    Raise:
        (RuntimeError): if len(observables) <= 0

    """

    if len(observables) <= 0:
        raise RuntimeError("#observables must be greather than zero")

    async def _subscribe(an_observer: Observer) -> Subscription:
        _source = list(observables)
        _current_subscription: Optional[Subscription] = None
        _observer: Optional[Observer] = None

        async def _on_completed() -> None:
            nonlocal _source, _current_subscription, _observer
            await _unsubscribe()
            if _source:
                obs = _source.pop(0)
                _current_subscription = await obs.subscribe(_observer)
            else:
                await an_observer.on_completed()
            return None

        async def _on_error(err: Any) -> None:
            await _unsubscribe()
            await an_observer.on_error(err=err)
            return None

        async def _unsubscribe() -> None:
            nonlocal _current_subscription

            if _current_subscription:
                await _current_subscription()
                _current_subscription = None

        _observer = rx_observer(on_next=an_observer.on_next, on_completed=_on_completed, on_error=_on_error)

        # initiate
        _current_subscription = await _source.pop(0).subscribe(_observer)

        return _unsubscribe

    return rx_create(subscribe=_subscribe, max_observer=1)
