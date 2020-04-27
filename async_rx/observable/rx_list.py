from collections import UserList
from typing import List, Optional

import curio

from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_list"]


class _RxList(UserList):
    def __init__(self, initlist: Optional[List] = None):
        self._event = curio.UniversalEvent()
        self._subscribers = 0
        super().__init__(initlist=initlist if initlist else [])

    async def subscribe(self, an_observer: Observer) -> Subscription:
        if self._subscribers > 0:
            raise RuntimeError("Only one subscription is supported")

        self._subscribers += 1

        _consumer_task = None

        async def consumer():
            try:
                while True:
                    await self._event.wait()
                    await an_observer.on_next(item=list(self.data))
                    self._event.clear()
            except curio.TaskCancelled:
                # it's time to finish
                pass

        async def _subscription():
            nonlocal _consumer_task
            if _consumer_task:
                await _consumer_task.cancel()
                _consumer_task = None
            self._subscribers -= 1

        _consumer_task = await curio.spawn(consumer())

        await an_observer.on_next(item=list(self.data))

        return _subscription

    def _set_event(self):
        if not self._event.is_set():
            self._event.set()

    def __setitem__(self, i, item):
        super().__setitem__(i, item)
        self._set_event()

    def __delitem__(self, i):
        super().__delitem__(i)
        self._set_event()

    def __add__(self, other):
        result = super().__add__(other)
        self._set_event()
        return rx_list(result)

    def __iadd__(self, other):
        super().__iadd__(other)
        self._set_event()
        return self

    def __mul__(self, n):
        result = super().__mul__(n)
        self._set_event()
        return rx_list(result)

    def __imul__(self, n):
        super().__imul__(n)
        self._set_event()
        return self

    def append(self, item):
        super().append(item)
        self._set_event()

    def insert(self, i, item):
        super().insert(i, item)
        self._set_event()

    def pop(self, i=-1):
        super().pop(i)
        self._set_event()

    def remove(self, item):
        super().remove(item)
        self._set_event()

    def clear(self):
        super().clear()
        self._set_event()

    def copy(self):
        return rx_list(super().copy())

    def reverse(self):
        super().reverse()
        self._set_event()

    def sort(self, *args, **kwds):
        super().sort(*args, **kwds)
        self._set_event()

    def extend(self, other):
        super().extend(other)
        self._set_event()


def rx_list(initial_value: Optional[List] = None) -> Observable:
    """Create an observable on list.

    The observer receive the current value of list on subscribe
    and when an item change (added, updated or deleted, ...).
    This observable implements a UserList, so you can use it as a classic list.

    Args:
        initial_value (Optional[List]): intial value (default: [])

    Returns:
        (Observable): observable instance

    """
    return _RxList(initlist=initial_value)
