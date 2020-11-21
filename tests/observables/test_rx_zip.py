import pytest

from async_rx import Observer, Subscription, rx_create, rx_from, rx_range, rx_zip
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_rx_zip_equals():

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=3), rx_from("abc"))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [(0, 'a'), (1, 'b'), (2, 'c')]


@pytest.mark.curio
async def test_rx_zip_limit_left():

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=2), rx_from("abc"))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 2
    assert seeker.items == [(0, 'a'), (1, 'b')]


@pytest.mark.curio
async def test_rx_zip_limit_right():

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=5), rx_from("abc"))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [(0, 'a'), (1, 'b'), (2, 'c')]


@pytest.mark.curio
async def test_rx_zip_with_error():
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_next("a")
        await an_observer.on_error("Oups")
        return default_subscription

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=3), rx_create(subscribe=_subscribe))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 1
    assert seeker.items == [(0, 'a')]
