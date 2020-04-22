"""Define rx_create."""
from typing import NoReturn, Optional, Union

from ..observer import ensure_observable_contract_operator
from ..protocol import Observable, ObservableDefinition, Observer, Subscribe, Subscription

__all__ = ["rx_create"]


def rx_create(subscribe: Subscribe, ensure_contract: Optional[bool] = True, max_observer: Optional[int] = None) -> Union[Observable, NoReturn]:
    """Create an observable with specific delayed execution 'subscribe'.

    Observables can be created with create, but usually we use the so-called
    creation operators, like of, from, interval, etc.
    Subscribing to an Observable is like calling a function, providing callbacks
    where the data will be delivered to.

    Args:
        subscribe (Subscribe): subcribe function to use on observable
        ensure_contract (bool): boolean flag (default True) to ensure that
            this observable will follow Observable contract.
        max_observer (int): maximum observer on this Observable (default None <=> unlimited)

    Returns:
        (Observable): an observable instance.

    Raise:
        (RuntimeError): if subscribe parameter is undefined

    """
    if subscribe is None:
        raise RuntimeError('a subscribe function must be provided')

    async def _subscribe(an_observer: Observer) -> Subscription:
        if ensure_contract:
            return await subscribe(ensure_observable_contract_operator(an_observer))
        return await subscribe(an_observer)

    if max_observer:
        # This limiter is probably a brain dead issue...
        # may we fix this disease later...
        current_observer = 0

        async def _subscribe_tracked(an_observer: Observer) -> Subscription:
            nonlocal current_observer

            if current_observer == max_observer:
                # TODO should we add NoReturn in Subscribe to manage this case ?
                raise RuntimeError(f'{max_observer} #observers limit reached')

            current_observer = current_observer + 1
            subscription = await _subscribe(an_observer)

            async def _unsubscribe():
                nonlocal current_observer
                current_observer = current_observer - 1
                return await subscription()

            return _unsubscribe

        return ObservableDefinition(subscribe=_subscribe_tracked)

    return ObservableDefinition(subscribe=_subscribe)
