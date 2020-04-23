"""Protocol definition."""
from collections import namedtuple
from typing import Any, NoReturn, Optional, Protocol, TypeVar, Union

__all__ = [
    'Subscription',
    'NextHandler',
    'CompleteHandler',
    'ErrorHandler',
    'Observable',
    'Observer',
    'Subscribe',
    'Subject',
    'ConnectableObservable',
    'ObserverDefinition',
    'ObservableDefinition',
    'SubjectDefinition',
    'ConnectableObservableDefinition',
    'ObservableFactory',
    'SubjectHandler',
    'ConnectableObservableHandler',
    'default_subscription',
    'PredicateOperator',
    'AccumulatorOperator',
    'SubjectFactory',
    'SubjectHandlerDefinition',
    'ConnectableObservableHandlerDefinition',
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
    """What is an Observer?

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


ObserverDefinition = namedtuple("Observer", ["on_next", "on_error", "on_completed"])
"""Implements Observer Protocol."""

ObservableDefinition = namedtuple("Observable", "subscribe")
"""Implements Observable Protocol."""

SubjectDefinition = namedtuple("Subject", ["subscribe", "on_next", "on_error", "on_completed"])
"""Implements Subject Protocol."""

ConnectableObservableDefinition = namedtuple("ConnectableObservable", ["connect", "ref_count", "subscribe"])
"""Implements ConnectableObservable Protocol."""

SubjectHandlerDefinition = namedtuple("SubjectHandler", ["on_subscribe", "on_unsubscribe"])
"""Implements SubjectHandler Protocol."""

ConnectableObservableHandlerDefinition = namedtuple("ConnectableObservableHandler", ["on_connect", "on_disconnect"])
"""Implements ConnectableObservableHandler Protocol."""


async def default_subscription() -> None:
    """Default subcribe implementation method.

    Do nothing.

    Returns:
        (None) - nothing to return.

    """
    pass
