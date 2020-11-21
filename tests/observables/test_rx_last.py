from typing import Any

import pytest

from async_rx import Observer, rx_last

from ..model import ObserverCounterCollector
from .model import get_observable


@pytest.mark.curio
async def test_rx_last_with_default():

    seeker = ObserverCounterCollector()

    sub = await rx_last(observable=get_observable()).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [99]


@pytest.mark.curio
async def test_rx_last():

    seeker = ObserverCounterCollector()

    sub = await rx_last(observable=get_observable(), count=5).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 5
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == list(range(95, 100))

    with pytest.raises(RuntimeError):
        rx_last(observable=get_observable(), count=0)

    with pytest.raises(RuntimeError):
        rx_last(observable=get_observable(), count=-1)
