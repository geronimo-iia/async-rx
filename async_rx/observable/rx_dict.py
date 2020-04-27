from collections import UserDict
from typing import Dict, Optional

import curio

from ..protocol import Observable, Observer, Subscription

__all__ = ["rx_dict"]


class _RxDict(UserDict):
    def __init__(self, dict: Dict):
        super(UserDict, self).__init__(dict=dict if dict else {})
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

    def __setitem__(self, key, item):
        self.data[key] = item
        self._event.set()

    def __delitem__(self, key):
        del self.data[key]
        self._event.set()


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
    return _RxDict(dict=initial_value)
