from typing import Any

import pytest

from async_rx import Observer, rx_distinct, rx_from

from ..model import ObserverCounterCollector
from .model import get_observable


@pytest.mark.curio
async def test_rx_distinct_dummy():
    seeker = ObserverCounterCollector()

    sub = await rx_distinct(observable=get_observable(), frame_size=3).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 100
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0:3] == [0, 1, 2]

    with pytest.raises(RuntimeError):
        rx_distinct(observable=get_observable(), frame_size=0)

    with pytest.raises(RuntimeError):
        rx_distinct(observable=get_observable(), frame_size=-1)


@pytest.mark.curio
async def test_rx_distinct():

    source = lambda: rx_from(observable_input=[1, 2, 1, 3, 2, 1, 4, 3, 2, 1, 5, 4, 3, 2, 1])

    seeker = ObserverCounterCollector()
    sub = await rx_distinct(observable=source(), frame_size=3).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 9
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3, 4, 1, 5, 3, 2, 1]

    seeker = ObserverCounterCollector()
    sub = await rx_distinct(observable=source(), frame_size=2).subscribe(an_observer=seeker)
    await sub()
    assert seeker.on_next_count == 13
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3, 1, 4, 3, 2, 1, 5, 4, 3, 2, 1]
