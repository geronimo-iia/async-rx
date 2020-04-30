"""Protocol definition."""
from typing import Any, NoReturn, Optional, Protocol, TypeVar, Union

__all__ = [
    "Subscription",
    "NextHandler",
    "CompleteHandler",
    "ErrorHandler",
    "Observable",
    "Observer",
    "Collector",
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

T = TypeVar('T')


class Subscription(Protocol):
    """Subscription Protocol.

    Subscription is a function to release resources or cancel Observable executions (act as a Disposable).
    It define something to be used and thrown away after you call it.
    """

    async def __call__(self) -> None:  # pragma: no cover
        """Release subscription."""
        pass


class NextHandler(Protocol):
    """NextHandler Protocol.

    A next handler process an item from associated observable.
    """

    async def __call__(self, item: Any) -> None:  # pragma: no cover
        """Process item."""
        pass


class CompleteHandler(Protocol):
    """CompleteHandler Protocol.

    A complete handler is call when no more item will came from the associated observable.
    """

    async def __call__(self) -> None:  # pragma: no cover
        """Signal completion of this observable."""
        pass


class ErrorHandler(Protocol):
    """ErrorHandler Protocol.

    An error handler receive a message or an exception and raise it.
    """

    async def __call__(self, err: Any) -> Optional[NoReturn]:  # pragma: no cover
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

    async def on_next(self, item: Any) -> None:  # pragma: no cover
        """Process item."""
        pass

    async def on_completed(self) -> None:  # pragma: no cover
        """Signal completion of this observable."""
        pass

    async def on_error(self, err: Any) -> Optional[NoReturn]:  # pragma: no cover
        pass


class Collector(Observer, Protocol):
    """Collector Observer Protocol."""

    def result(self) -> Any:  # pragma: no cover
        """Returns result."""
        pass

    def is_finish(self) -> bool:  # pragma: no cover
        """Return true if observable has completed."""
        pass

    def has_error(self) -> bool:  # pragma: no cover
        """Return true if observable has meet error."""
        pass

    def error(self) -> Any:  # pragma: no cover
        """Return error if observable has meet error."""
        pass


class Subscribe(Protocol):
    """Subscribe Protocol.

    It's a (sync/async) function wich take an observer and return a subscription.
    """

    async def __call__(self, an_observer: Observer) -> Subscription:  # pragma: no cover
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

    async def subscribe(self, an_observer: Observer) -> Subscription:  # pragma: no cover
        pass


class ObservableFactory(Protocol):
    """Async ObservableFactory Protocol.

    Define function which create Observable.
    """

    async def __call__(self) -> Observable:  # pragma: no cover
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

    async def __call__(self, count: int, source: Observer) -> None:  # pragma: no cover
        pass


class SubjectHandler(Protocol):
    """Subscribe Handler Protocol.

    This handler could be called on subscription/unsubscribe event.
    """

    async def on_subscribe(self, count: int, source: Observer) -> None:  # pragma: no cover
        """Notify on subscribe event.

        Args:
            count (int): current #subscribers after subscription
            source (Observer): observer source

        """
        pass

    async def on_unsubscribe(self, count: int, source: Observer) -> None:  # pragma: no cover
        """Notify on unsubscribe event.

        Args:
            count (int): current #subscribers after unsubscribe
            source (Observer): observer source

        """
        pass


class SubjectFactory(Protocol):
    def __call__(self, subject_handler: Optional[SubjectHandler] = None) -> Subject:  # pragma: no cover
        pass


class ConnectHandler(Protocol):
    """Connect Handler Protocol."""

    async def __call__(self) -> Subscription:  # pragma: no cover
        pass


class RefCountHandler(Protocol):
    """RefCount Handler Protocol."""

    async def __call__(self) -> Observable:  # pragma: no cover
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

    async def connect(self) -> Subscription:  # pragma: no cover
        """Connect."""
        pass

    async def ref_count(self) -> Observable:  # pragma: no cover
        """Reference counter.

        Make the multicasted Observable automatically start executing when
        the first subscriber arrives,
        and stop executing when the last subscriber leaves.
        """
        pass


class ConnectableObservableEventHandler(Protocol):
    """Connectable Observable Event Handler Protocol."""

    async def __call__(self) -> None:  # pragma: no cover
        pass


class ConnectableObservableHandler(Protocol):
    """Connectable Observable Handler Protocol.

    This handler could be called on conect/disconnect event.
    """

    async def on_connect(self) -> None:  # pragma: no cover
        """Called on connect event."""
        pass

    async def on_disconnect(self) -> None:  # pragma: no cover
        """Called on disconnect event."""
        pass


class _AsyncAccumulatorOperator(Protocol[T]):
    """Async Accumulator Operator Protocol.

    Accumulator are used in reduce operation.
    """

    async def __call__(self, buffer: T, item: T) -> T:  # pragma: no cover
        pass


class _SyncAccumulatorOperator(Protocol[T]):
    """Async Accumulator Operator Protocol.

    Accumulator are used in reduce operation.
    """

    def __call__(self, buffer: T, item: T) -> T:  # pragma: no cover
        pass


AccumulatorOperator = Union[_AsyncAccumulatorOperator, _SyncAccumulatorOperator]
"""Accumulator Operator Protocol.

Accumulator are used in reduce operation.
"""


class _AsyncPredicateOperator(Protocol):
    """Async Predicate Operator Protocol.

    Predicate are used in filter operation.
    """

    async def __call__(self, item: Any) -> bool:  # pragma: no cover
        pass


class _SyncPredicateOperator(Protocol):
    """Sync Predicate Operator Protocol.

    Predicate are used in filter operation.
    """

    def __call__(self, item: Any) -> bool:  # pragma: no cover
        pass


PredicateOperator = Union[_AsyncPredicateOperator, _SyncPredicateOperator]
"""Predicate Operator Protocol.

Predicate are used in filter operation.
"""
