import curio
from typing import Optional, List
from collections import UserList
from ..protocol import Observable, Observer, Subscription


__all__ = ["rx_list"]


class _RxList(UserList):
    def __init__(self, initlist: Optional[List] = None):
        super(UserList, self).__init__(initlist=initlist if initlist else [])
        self._event = curio.UniversalEvent()

    async def subscribe(self, an_observer: Observer) -> Subscription:
        _consumer_task = None

        async def consumer():
            try:
                while True:
                    await self._event.wait()
                    await an_observer.on_next(item=self.data)
            except curio.TaskCancelled:
                # it's time to finish
                pass

        async def _subscription():
            nonlocal _consumer_task
            if _consumer_task:
                await _consumer_task.cancel()
                _consumer_task = None

        _consumer_task = await curio.spawn(consumer())

        return _subscription

    def __setitem__(self, i, item):
        super(self).__setitem__(i, item)
        self._event.set()

    def __delitem__(self, i):
        super(self).__delitem__(i)
        self._event.set()

    def __add__(self, other):
        result = super(self).__add__(other)
        self._event.set()
        return result

    def __radd__(self, other):
        result = super(self).__radd__(other)
        self._event.set()
        return result

    def __iadd__(self, other):
        super(self).__iadd__(other)
        self._event.set()
        return self

    def __mul__(self, n):
        result = super(self).__mul__(n)
        self._event.set()
        return result

    def __imul__(self, n):
        super(self).__imul__(n)
        self._event.set()
        return self


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
