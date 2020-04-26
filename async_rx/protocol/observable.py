"""Observable utilities."""

from collections import namedtuple
from typing import Any, NoReturn, Optional

from .definition import Observable, Observer, Subscribe, Subscription
from .observer import rx_observer

__all__ = ["observable", "ensure_observable_contract_operator"]

_ObservableDefinition = namedtuple("Observable", "subscribe")
"""Implements Observable Protocol."""


def observable(subscribe: Subscribe, ensure_contract: Optional[bool] = True) -> Observable:
    """Build an observable.

    The underlying implementation use an named tuple.

    Args:
        subscribe (Subscribe): subcribe function to use on observable
        ensure_contract (bool): boolean flag (default True) to ensure that
            this observable will follow Observable contract.

    Returns:
        (Observable): an observable

    Raise:
        (RuntimeError): if subscribe parameter is undefined

    """
    if subscribe is None:
        raise RuntimeError('a subscribe function must be provided')

    async def _subscribe(an_observer: Observer) -> Subscription:
        if ensure_contract:
            return await subscribe(ensure_observable_contract_operator(an_observer))
        return await subscribe(an_observer)

    return _ObservableDefinition(subscribe=_subscribe)


def ensure_observable_contract_operator(an_observer: Observer) -> Observer:
    """Ensure Observable Grammar or Contract.

    ```next*(error|complete)?```

    In an Observable Execution, zero to infinite Next notifications may be delivered.
    If either an Error or Complete notification is delivered, then nothing else
    can be delivered afterwards.

    Args;
        an_observer (Observer): the observer which must be ensure that subscribed
            observable follow contract.

    Returns:
        (Observer): an Observer which follow the contract.

    """
    _deliver_next = True

    async def _on_next(item: Any) -> None:
        nonlocal _deliver_next

        if _deliver_next:
            await an_observer.on_next(item)

    async def _on_error(err: Any) -> Optional[NoReturn]:  # type: ignore
        nonlocal _deliver_next

        if _deliver_next:
            _deliver_next = False
            await an_observer.on_error(err)

    async def _on_completed() -> None:
        nonlocal _deliver_next

        if _deliver_next:
            _deliver_next = False
            await an_observer.on_completed()

    return rx_observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed)
