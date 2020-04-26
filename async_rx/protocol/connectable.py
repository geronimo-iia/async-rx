"""Connectable Observable utilities."""

from collections import namedtuple

from .definition import ConnectableObservable, ConnectableObservableEventHandler, ConnectableObservableHandler, ConnectHandler, RefCountHandler, Subscribe

__all__ = ["connectable_observable", "connectable_observable_handler"]


_ConnectableObservableDefinition = namedtuple("ConnectableObservable", ["connect", "ref_count", "subscribe"])
"""Implements ConnectableObservable Protocol."""

_ConnectableObservableHandlerDefinition = namedtuple("ConnectableObservableHandler", ["on_connect", "on_disconnect"])
"""Implements ConnectableObservableHandler Protocol."""


def connectable_observable(connect: ConnectHandler, ref_count: RefCountHandler, subscribe: Subscribe) -> ConnectableObservable:
    return _ConnectableObservableDefinition(connect=connect, ref_count=ref_count, subscribe=subscribe)


def connectable_observable_handler(
    on_connect: ConnectableObservableEventHandler, on_disconnect: ConnectableObservableEventHandler
) -> ConnectableObservableHandler:
    return _ConnectableObservableHandlerDefinition(on_connect=on_connect, on_disconnect=on_disconnect)
