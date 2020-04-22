"""Protocol definition and implementation root."""
from collections import namedtuple
from typing import Any, NoReturn, Protocol, Union

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

    async def __call__(self, err: Union[Any, Exception]) -> Union[NoReturn, None]:
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

    async def on_error(self, err: Union[Any, Exception]) -> Union[NoReturn, None]:
        raise RuntimeError("")


class Subscribe(Protocol):
    """Subscribe Protocol.

    It's a (sync/async) function wich take an observer and return a subscription.
    """

    async def __call__(self, observer: Observer) -> Subscription:
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

    async def subscribe(self, observer: Observer) -> Subscription:
        pass


class Subject(Observable, Observer, Protocol):
    """A Subject is like an Observable, but can multicast to many Observers.

    Subjects are like EventEmitters: they maintain a registry of many listeners.
    """

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


ObserverDefinition = namedtuple("Observer", ["on_next", "on_error", "on_completed"])
"""Implements Observer Protocol."""

ObservableDefinition = namedtuple("Observable", "subscribe")
"""Implements Observable Protocol."""

SubjectDefinition = namedtuple("Subject", ObservableDefinition._fields + ObserverDefinition._fields)  # type: ignore
"""Implements Subject Protocol."""

ConnectableObservableDefinition = namedtuple("ConnectableObservable", ("connect", "ref_count") + ObservableDefinition._fields)  # type: ignore
"""Implements ConnectableObservable Protocol."""
