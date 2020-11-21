from typing import Any

import pytest

from async_rx import Observer, rx_first, rx_from

from ..model import ObserverCounterCollector
from .model import get_observable


@pytest.mark.curio
async def test_rx_first():

    seeker = ObserverCounterCollector()

    sub = await rx_first(observable=get_observable()).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [0]


@pytest.mark.curio
async def test_rx_first_with_just_one():

    seeker = ObserverCounterCollector()

    sub = await rx_first(observable=rx_from("A")).subscribe(an_observer=seeker)
    await sub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == ["A"]
