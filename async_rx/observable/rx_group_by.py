from inspect import iscoroutinefunction
from typing import Any, Callable, Dict

from ..protocol import Observable, Observer, Subject, Subscription, rx_observer
from ..subject import rx_subject
from .rx_create import rx_create

__all__ = ["rx_group_by"]


def rx_group_by(observable: Observable, key_selector: Callable) -> Observable:
    """Group by operator.

    Similar to Window, GroupBy projects the sequence onto a number of inner observables
    but as opposite to Window where all windows receive the same sequence,
    GroupBy will emit elements only to one inner observable that is associated
    with the current element based on a key selector function.
    The observer receive tuple with (key, subject).

    Args:
        observable (Observable): observable instance
        key_selector (Callable): key selector function (sync/async) [Any]->[Any]

    Returns:
        (Observable): observable instance

    """
    _is_awaitable = iscoroutinefunction(key_selector)

    async def _subscribe(an_observer: Observer) -> Subscription:

        _observables: Dict[Any, Subject] = {}

        async def _on_next(item: Any):
            nonlocal _observables, _is_awaitable
            key = await key_selector(item) if _is_awaitable else key_selector(item)
            if key not in _observables:
                _observables[key] = rx_subject()
                await an_observer.on_next(item=(key, _observables[key]))
            await _observables[key].on_next(item=item)

        async def _on_completed():
            nonlocal _observables
            for _, o in _observables.items():
                await o.on_completed()
            await an_observer.on_completed()

        async def _on_error(err: Any):
            nonlocal _observables
            for _, o in _observables.items():
                try:
                    await o.on_error(err=err)
                except Exception:
                    pass
            await an_observer.on_error(err=err)
            return None

        return await observable.subscribe(rx_observer(on_next=_on_next, on_completed=_on_completed, on_error=_on_error))

    return rx_create(subscribe=_subscribe, max_observer=1)
