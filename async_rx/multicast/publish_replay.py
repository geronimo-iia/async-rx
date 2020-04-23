from typing import Optional

from ..protocol import ConnectableObservable, ConnectableObservableHandler, Observable, Subject, SubjectHandler
from ..subject import replay_subject
from .multicast import multicast

__all__ = ["publish_replay"]


def publish_replay(
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
        return replay_subject(buffer_size=buffer_size, subject_handler=subject_handler)

    return multicast(subject_factory=_subject_factory, an_observable=an_observable, subject_handler=subject_handler, connection_handler=connection_handler)
