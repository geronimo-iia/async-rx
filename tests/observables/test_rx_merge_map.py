import curio
import pytest

from async_rx import Observer, Subscription, rx_create, rx_from, rx_merge_map, rx_range
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import countdown


@pytest.mark.curio
async def test_rx_merge_map():

    seeker = ObserverCounterCollector()

    async def adder(i):
        return i + 1

    async def _build():
        return rx_merge_map(rx_create(subscribe=await countdown(2, 0.1)), rx_create(subscribe=await countdown(2, 0.2)), transform=adder)

    obs = await _build()
    sub_a = await obs.subscribe(seeker)
    await sub_a()
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 4
    assert seeker.items == [3, 3, 2, 2]


@pytest.mark.curio
async def test_rx_merge_map_sync():

    seeker = ObserverCounterCollector()

    def adder(i):
        return i + 1

    async def _build():
        return rx_merge_map(rx_create(subscribe=await countdown(2, 0.1)), rx_create(subscribe=await countdown(2, 0.2)), transform=adder)

    obs = await _build()
    sub_a = await obs.subscribe(seeker)
    await sub_a()
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 4
    assert seeker.items == [3, 3, 2, 2]
