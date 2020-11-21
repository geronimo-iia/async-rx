import pytest

from async_rx import Observer, Subscription, rx_buffer, rx_create, rx_empty, rx_from, rx_range
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


def test_rx_buffer_default():
    with pytest.raises(RuntimeError):
        rx_buffer(observable=rx_empty(), buffer_size=0)
    with pytest.raises(RuntimeError):
        rx_buffer(observable=rx_empty(), buffer_size=-1)


@pytest.mark.curio
async def test_rx_buffer():

    seeker = ObserverCounterCollector()

    obs = rx_buffer(rx_range(start=1, stop=20), buffer_size=5)
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]


@pytest.mark.curio
async def test_rx_buffer_with_error():
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_next(1)
        await an_observer.on_next(2)
        await an_observer.on_next(3)
        await an_observer.on_next(4)
        await an_observer.on_next(5)
        await an_observer.on_error("oups")
        return default_subscription

    seeker = ObserverCounterCollector()

    obs = rx_buffer(rx_create(subscribe=_subscribe), buffer_size=2)
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 2
    assert seeker.items == [[1, 2], [3, 4]]
