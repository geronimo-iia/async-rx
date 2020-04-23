from typing import Optional

from ..protocol import ConnectableObservable, ConnectableObservableHandler, Observable, SubjectHandler
from ..subject import behavior_subject
from .multicast import multicast

__all__ = ["publish_behavior"]


def publish_behavior(
    an_observable: Observable, subject_handler: Optional[SubjectHandler] = None, connection_handler: Optional[ConnectableObservableHandler] = None
) -> ConnectableObservable:
    """Create a publish_behavior.

    A publish_behavior uses a behavior_subject under the hood to make multiple
    Observers see the same Observable execution.

    Args:
        an_observable (Observable): observable to connect
        subject_handler (Optional[SubjectHandler]): optional subject handler
        connection_handler (Optional[ConnectableObservableHandler]): optional connection handler

    Returns:
        (ConnectableObservable): the publish_behavior instance

    """
    return multicast(subject_factory=behavior_subject, an_observable=an_observable, subject_handler=subject_handler, connection_handler=connection_handler)
