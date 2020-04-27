import pytest
import curio
from async_rx import Observer, rx_create, rx_from, rx_merge_map, rx_range, Subscription
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import countdown


def test_rx_merge_map(kernel):

    seeker = ObserverCounterCollector()

    async def adder(i):
        return i + 1

    async def _build():
        return rx_merge_map(rx_create(subscribe=await countdown(2, 0.1)), rx_create(subscribe=await countdown(2, 0.2)), transform=adder)

    obs = kernel.run(_build())
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 4
    assert seeker.items == [3, 3, 2, 2]


def test_rx_merge_map_sync(kernel):

    seeker = ObserverCounterCollector()

    def adder(i):
        return i + 1

    async def _build():
        return rx_merge_map(rx_create(subscribe=await countdown(2, 0.1)), rx_create(subscribe=await countdown(2, 0.2)), transform=adder)

    obs = kernel.run(_build())
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 4
    assert seeker.items == [3, 3, 2, 2]
