from typing import Any

import pytest

from async_rx import Observer, rx_filter

from ..model import ObserverCounterCollector
from .model import get_observable


@pytest.mark.curio
async def test_rx_filter():
    async def _predicate(item: int) -> bool:
        return item % 2 == 0

    seeker = ObserverCounterCollector()

    sub = await rx_filter(observable=get_observable(), predicate=_predicate).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 50
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0:6] == [0, 2, 4, 6, 8, 10]
