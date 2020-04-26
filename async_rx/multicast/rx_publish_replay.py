from typing import Optional

from ..protocol import ConnectableObservable, ConnectableObservableHandler, Observable, Subject, SubjectHandler
from ..subject import rx_subject_replay
from .rx_publish import rx_publish

__all__ = ["rx_publish_replay"]


def rx_publish_replay(
    an_observable: Observable,
    buffer_size: int,
    subject_handler: Optional[SubjectHandler] = None,
    connection_handler: Optional[ConnectableObservableHandler] = None,
) -> ConnectableObservable:
    """Create a publish_replay.

    A publish_replay uses a replay_subject under the hood to make
    multiple Observers see the same Observable execution.

    Args:
        buffer_size (int): max #items to replay
        an_observable (Observable): observable to connect
        subject_handler (Optional[SubjectHandler]): optional subject handler
        connection_handler (Optional[ConnectableObservableHandler]): optional connection handler

    Returns:
        (ConnectableObservable): the publish_replay instance

    """

    def _subject_factory(subject_handler: Optional[SubjectHandler] = None) -> Subject:
        return rx_subject_replay(buffer_size=buffer_size, subject_handler=subject_handler)

    return rx_publish(subject_factory=_subject_factory, an_observable=an_observable, subject_handler=subject_handler, connection_handler=connection_handler)
