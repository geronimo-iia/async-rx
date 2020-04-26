from typing import Optional

from ..observable import rx_create
from ..protocol import (
    ConnectableObservable,
    ConnectableObservableHandler,
    Observable,
    Observer,
    Subject,
    SubjectFactory,
    SubjectHandler,
    Subscription,
    subject_handler as _subject_handler,
    connectable_observable
)
from ..subject import rx_subject

__all__ = ["rx_publish"]


def rx_publish(
    an_observable: Observable,
    subject_handler: Optional[SubjectHandler] = None,
    connection_handler: Optional[ConnectableObservableHandler] = None,
    subject_factory: SubjectFactory = rx_subject,
) -> ConnectableObservable:
    """Create a Connectable Observable.

    A multicasted Observable (rx_publish) uses a Subject under the hood to make multiple
    Observers see the same Observable execution.

    Args:
        an_observable (Observable): observable to connect
        subject_handler (Optional[SubjectHandler]): optional subject handler
        connection_handler (Optional[ConnectableObservableHandler]): optional connection handler
        subject_factory (Optional[SubjectFactory]): subject factory, per default use subject

    Returns:
        (ConnectableObservable): the multicasted Observable instance

    """
    _ref_count_activated = False  # Flag to enable auto-connect
    _ref_count = 0  # subscription count (used for auto-connect)
    _subscription: Optional[Subscription] = None  # observale subscription
    _connectable_observable: Optional[ConnectableObservable] = None  # for ref_count return value
    _subject: Optional[Subject] = None

    async def _unsubscribe() -> None:
        nonlocal _subscription

        if _subscription:
            await _subscription()
            # notify
            if connection_handler:
                await connection_handler.on_disconnect()

            _subscription = None

    async def _connect() -> Subscription:
        """Connection Handler implementation."""
        nonlocal _subscription, _subject

        if _subscription:
            return _unsubscribe

        if not _subject:
            # never reached
            raise RuntimeError("unexpected error")

        _subscription = await an_observable.subscribe(an_observer=_subject)

        if connection_handler:
            await connection_handler.on_connect()

        return _unsubscribe

    async def _on_subscribe(count: int, source: Observer) -> None:
        nonlocal _subscription, _ref_count_activated, _ref_count

        _ref_count += 1

        # forward event
        if subject_handler:
            await subject_handler.on_subscribe(count=count, source=source)

        # auto connect
        if _ref_count_activated and _subscription is None and _ref_count == 1:
            await _connect()

    async def _on_unsubscribe(count: int, source: Observer) -> None:
        nonlocal _subscription, _ref_count_activated, _ref_count

        _ref_count -= 1

        # forward event
        if subject_handler:
            await subject_handler.on_unsubscribe(count=count, source=source)

        # auto disconnect
        if _ref_count_activated and _subscription and _ref_count == 0:
            await _unsubscribe()

    # our multicast subject used under the hood
    _subject = subject_factory(subject_handler=_subject_handler(on_subscribe=_on_subscribe, on_unsubscribe=_on_unsubscribe))

    def _ref_count_handler() -> Observable:
        """Autostart the multicasted observable.

        ref_count makes the multicasted Observable automatically start executing when
        the first subscriber arrives,
        and stop executing when the last subscriber leaves.
        """
        nonlocal _ref_count_activated, _connectable_observable

        if not _connectable_observable:
            # never reached
            raise RuntimeError("unexpected error")

        _ref_count_activated = True

        return rx_create(subscribe=_connectable_observable.subscribe)

    # our connectable observable
    _connectable_observable = connectable_observable(connect=_connect, ref_count=_ref_count_handler, subscribe=_subject.subscribe)

    return _connectable_observable
