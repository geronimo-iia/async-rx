from collections import UserDict
from typing import Dict, Optional, Union

import curio

from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_dict"]


class _RxDict(UserDict):
    def __init__(self, dict: Union[Dict, "_RxDict"]):
        self._event = curio.UniversalEvent()
        self._subscribers = 0
        super().__init__(dict)

    async def subscribe(self, an_observer: Observer) -> Subscription:

        if self._subscribers > 0:
            raise RuntimeError("Only one subscription is supported")

        self._subscribers += 1

        _consumer_task = None

        async def consumer():
            try:
                while True:
                    await self._event.wait()
                    await an_observer.on_next(item=dict(self.data))
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

        await an_observer.on_next(item=dict(self.data))

        return _subscription

    def _set_event(self):
        if not self._event.is_set() and self._subscribers:
            self._event.set()

    def __setitem__(self, key, item):
        self.data[key] = item
        self._set_event()

    def __delitem__(self, key):
        del self.data[key]
        self._set_event()

    def copy(self):
        return _RxDict(super().copy())


def rx_dict(initial_value: Optional[Dict] = None) -> Observable:
    """Create an observable on dictionnary.

    The observer receive the current value of dictionnary on subscribe
    and when a key change (added, updated or deleted).
    This observable implements a UserDict, so you can use it as a classic dictionnary.

    Args:
        initial_value (Optional[Dict]): intial value (default: {})

    Returns:
        (Observable): observable instance

    """
    return _RxDict(dict=initial_value if initial_value else {})
