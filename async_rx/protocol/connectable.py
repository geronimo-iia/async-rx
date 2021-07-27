"""Connectable Observable utilities."""

from collections import namedtuple

from .definition import ConnectableObservable, ConnectableObservableEventHandler, ConnectableObservableHandler, ConnectHandler, RefCountHandler, Subscribe

__all__ = ["connectable_observable", "connectable_observable_handler"]


ConnectableObservableDefinition = namedtuple("ConnectableObservableDefinition", ["connect", "ref_count", "subscribe"])
"""Implements ConnectableObservable Protocol."""

ConnectableObservableHandlerDefinition = namedtuple("ConnectableObservableHandlerDefinition", ["on_connect", "on_disconnect"])
"""Implements ConnectableObservableHandler Protocol."""


def connectable_observable(connect: ConnectHandler, ref_count: RefCountHandler, subscribe: Subscribe) -> ConnectableObservable:
    return ConnectableObservableDefinition(connect=connect, ref_count=ref_count, subscribe=subscribe)


def connectable_observable_handler(
    on_connect: ConnectableObservableEventHandler, on_disconnect: ConnectableObservableEventHandler
) -> ConnectableObservableHandler:
    return ConnectableObservableHandlerDefinition(on_connect=on_connect, on_disconnect=on_disconnect)
