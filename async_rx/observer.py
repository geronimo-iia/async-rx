"""Observer protocol implementation."""
from typing import Any, NoReturn, Union

from .protocol import CompleteHandler, ErrorHandler, NextHandler, Observer, ObserverDefinition

__all__ = ['observer', 'default_on_completed', 'default_error', 'ensure_observable_contract_operator']


async def default_on_completed() -> None:
    """Default on complet handler.

    No operation.

    Returns:
        (None): nothing

    """
    pass


async def default_error(err: Union[Any, Exception]) -> NoReturn:
    """Always raise error.

    It's our default error handler implementation.
    """
    if isinstance(err, BaseException):
        raise err

    raise Exception(err)


def observer(on_next: NextHandler, on_error: ErrorHandler = default_error, on_completed: CompleteHandler = default_on_completed) -> Observer:
    """Return an observer.

    The underlying implementation use an ObserverDefinition named tuple.

    Args:
        on_next (NextHandler): on_next handler which process items
        on_error (ErrorHandler): on_error handler (default with default_error
            which raise Exception)
        on_completed (CompleteHandler): on_completed handler (default with noop)

    Returns:
        (Observer): an Observer

    """
    return ObserverDefinition(on_next=on_next, on_error=on_error, on_completed=on_completed)


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
    deliver_next = True

    async def _on_next(item: Any) -> None:
        nonlocal deliver_next

        if deliver_next:
            await an_observer.on_next(item)

    async def _on_error(err: Union[Any, Exception]) -> Union[NoReturn, None]:  # type: ignore
        nonlocal deliver_next

        if deliver_next:
            deliver_next = False
            await an_observer.on_error(err)

    async def _on_completed() -> None:
        nonlocal deliver_next

        if deliver_next:
            deliver_next = False
            await an_observer.on_completed()

    return observer(on_next=_on_next, on_error=_on_error, on_completed=_on_completed)
