"""Protocol definition."""
from typing import Any, NoReturn, Optional, Protocol, TypeVar, Union

__all__ = [
    "Subscription",
    "NextHandler",
    "CompleteHandler",
    "ErrorHandler",
    "Observable",
    "Observer",
    "Subscribe",
    "Subject",
    "ConnectHandler",
    "RefCountHandler",
    "ConnectableObservable",
    "ObservableFactory",
    "SubjectEventHandler",
    "SubjectHandler",
    "ConnectableObservableEventHandler",
    "ConnectableObservableHandler",
    "PredicateOperator",
    "AccumulatorOperator",
    "SubjectFactory",
]


class Subscription(Protocol):
    """Subscription Protocol.

    Subscription is a function to release resources or cancel Observable executions (act as a Disposable).
    It define something to be used and thrown away after you call it.
    """

    async def __call__(self) -> None:
        """Release subscription."""
        pass


class NextHandler(Protocol):
    """NextHandler Protocol.

    A next handler process an item from associated observable.
    """

    async def __call__(self, item: Any) -> None:
        """Process item."""
        pass


class CompleteHandler(Protocol):
    """CompleteHandler Protocol.

    A complete handler is call when no more item will came from the associated observable.
    """

    async def __call__(self) -> None:
        """Signal completion of this observable."""
        pass


class ErrorHandler(Protocol):
    """ErrorHandler Protocol.

    An error handler receive a message or an exception and raise it.
    """

    async def __call__(self, err: Any) -> Optional[NoReturn]:
        """Raise error.

        Args:
            err (Union[Any, Exception]): the error to raise

        Raises:
            (Exception): the exception

        """
        pass


class Observer(Protocol):
    """Observer Protocol.

    What is an Observer?

    An Observer is a consumer of values delivered by an Observable.

    Observers are simply a set of callbacks, one for each type of notification
    delivered by the Observable:

    - next,
    - error,
    - and complete.

    Observers are just "objects" with three callbacks, one for each type of
    notification that an Observable may deliver.
    """

    async def on_next(self, item: Any) -> None:
        """Process item."""
        pass

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        pass

    async def on_error(self, err: Any) -> Optional[NoReturn]:
        pass


class Subscribe(Protocol):
    """Subscribe Protocol.

    It's a (sync/async) function wich take an observer and return a subscription.
    """

    async def __call__(self, an_observer: Observer) -> Subscription:
        """Implement observer subscription.

        Args:
            observer (Observer): the observer instance

        Returns:
            (Subscription): subscription

        """
        pass


class Observable(Protocol):
    """Observable Protocol.

    An observable is something on which we can subscribe to listen event.
    """

    async def subscribe(self, an_observer: Observer) -> Subscription:
        pass


class ObservableFactory(Protocol):
    """Async ObservableFactory Protocol.

    Define function which create Observable.
    """

    async def __call__(self) -> Observable:
        """Create an Observable.

        Returns:
            (Observable): the new observable instance.

        """
        pass


class Subject(Observable, Observer, Protocol):
    """A Subject is like an Observable, but can multicast to many Observers.

    Subjects are like EventEmitters: they maintain a registry of many listeners.
    """

    pass


class SubjectEventHandler(Protocol):
    """Subject Event Handler Procotol."""

    async def __call__(self, count: int, source: Observer) -> None:
        pass


class SubjectHandler(Protocol):
    """Subscribe Handler Protocol.

    This handler could be called on subscription/unsubscribe event.
    """

    async def on_subscribe(self, count: int, source: Observer) -> None:
        """Notify on subscribe event.

        Args:
            count (int): current #subscribers after subscription
            source (Observer): observer source

        """
        pass

    async def on_unsubscribe(self, count: int, source: Observer) -> None:
        """Notify on unsubscribe event.

        Args:
            count (int): current #subscribers after unsubscribe
            source (Observer): observer source

        """
        pass


class SubjectFactory(Protocol):
    def __call__(self, subject_handler: Optional[SubjectHandler] = None) -> Subject:
        pass


class ConnectHandler(Protocol):
    """Connect Handler Protocol."""

    async def __call__(self) -> Subscription:
        pass


class RefCountHandler(Protocol):
    """RefCount Handler Protocol."""

    async def __call__(self) -> Observable:
        pass


class ConnectableObservable(Observable, Protocol):
    """Define a connectable observable protocol.

    We have :
        - subscribe function (it's an observable)
        - connect function: start executing
        - ref_count function: makes the Observable automatically start executing
            when the first subscriber arrives,
            and stop executing when the last subscriber leaves.
    """

    async def connect(self) -> Subscription:
        """Connect."""
        pass

    async def ref_count(self) -> Observable:
        """Reference counter.

        Make the multicasted Observable automatically start executing when
        the first subscriber arrives,
        and stop executing when the last subscriber leaves.
        """
        pass


class ConnectableObservableEventHandler(Protocol):
    """Connectable Observable Event Handler Protocol."""

    async def __call__(self) -> None:
        pass


class ConnectableObservableHandler(Protocol):
    """Connectable Observable Handler Protocol.

    This handler could be called on conect/disconnect event.
    """

    async def on_connect(self) -> None:
        """Called on connect event."""
        pass

    async def on_disconnect(self) -> None:
        """Called on disconnect event."""
        pass


T = TypeVar('T')


class AsyncAccumulatorOperator(Protocol[T]):
    """Async Accumulator Operator Protocol.

    Accumulator are used in reduce operation.
    """

    async def __call__(self, buffer: T, item: T) -> T:
        pass


class SyncAccumulatorOperator(Protocol[T]):
    """Async Accumulator Operator Protocol.

    Accumulator are used in reduce operation.
    """

    def __call__(self, buffer: T, item: T) -> T:
        pass


AccumulatorOperator = Union[AsyncAccumulatorOperator, SyncAccumulatorOperator]
"""Accumulator Operator Protocol.

Accumulator are used in reduce operation.
"""


class PredicateOperator(Protocol):
    """Predicate Operator Protocol.

    Predicate ae used in filter operation.
    """

    async def __call__(self, item: Any) -> bool:
        pass
