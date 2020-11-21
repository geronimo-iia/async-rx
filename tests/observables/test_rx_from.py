import pytest

from async_rx import Observable, Observer, rx_create, rx_from
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_rx_from_dict():
    result = rx_from({"A": True})
    assert hasattr(result, "subscribe")
    result["B"] = False
    assert result == {"A": True, "B": False}


@pytest.mark.curio
async def test_rx_from_iterable():

    obs: Observable = rx_from(observable_input=[1, 2, 3])

    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 3
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3]


@pytest.mark.curio
async def test_rx_from_observable():
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    obs: Observable = rx_from(observable_input=rx_create(subscribe=_subscribe))
    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1]


@pytest.mark.curio
async def test_rx_from_slug():
    class Temp:
        async def subscribe(self, an_observer: Observer):
            await an_observer.on_next(item=1)
            await an_observer.on_completed()
            return default_subscription

    obs: Observable = rx_from(observable_input=Temp())
    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1]


@pytest.mark.curio
async def test_rx_from_singleton():

    obs: Observable = rx_from(observable_input=42)
    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [42]


@pytest.mark.curio
async def test_rx_from_awaitable_iterable():
    async def generate():
        for i in range(4):
            yield i

    obs: Observable = rx_from(observable_input=generate())
    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 4
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [0, 1, 2, 3]
