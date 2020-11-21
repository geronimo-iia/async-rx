import curio
import pytest

from async_rx import Observer, Subscription, rx_amb, rx_create, rx_from, rx_range
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import countdown


def test_rx_amb_init():
    with pytest.raises(RuntimeError):
        rx_amb()


@pytest.mark.curio
async def test_rx_amb():

    seeker = ObserverCounterCollector()

    a = rx_create(subscribe=await countdown(5, 0.1))
    b = rx_create(subscribe=await countdown(10, 0.2))

    obs = rx_amb(a, b)
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [a]


@pytest.mark.curio
async def test_rx_amb2():

    seeker = ObserverCounterCollector()

    a = rx_create(subscribe=await countdown(5, 0.1))
    b = rx_create(subscribe=await countdown(10, 0.05))

    obs = rx_amb(a, b)
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [b]


@pytest.mark.curio
async def test_rx_amb_with_error():

    seeker = ObserverCounterCollector()

    async def _subscribe(an_observer: Observer) -> Subscription:
        await curio.sleep(0.05)
        await an_observer.on_error(err="Args")
        return default_subscription

    a = rx_create(subscribe=await countdown(5, 0.1))

    obs = rx_amb(a, rx_create(subscribe=_subscribe))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [a]
