import pytest

from ..model import ObserverCounterCollector
from async_rx.protocol import Observer, Observable
from async_rx.observable import rx_from, rx_create, default_subscription


def test_rx_from_iterable(kernel):

    obs: Observable = rx_from(observable_input=[1, 2, 3])

    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 3
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3]


def test_rx_from_observable(kernel):
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    obs: Observable = rx_from(observable_input=rx_create(subscribe=_subscribe))
    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1]


def test_rx_from_slug(kernel):
    class Temp:
        async def subscribe(self, an_observer: Observer):
            await an_observer.on_next(item=1)
            await an_observer.on_completed()
            return default_subscription

    obs: Observable = rx_from(observable_input=Temp())
    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1]


def test_rx_from_singleton(kernel):

    obs: Observable = rx_from(observable_input=42)
    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [42]


def test_rx_from_awaitable_iterable(kernel):
    async def generate():
        for i in range(4):
            yield i

    obs: Observable = rx_from(observable_input=generate())
    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 4
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [0, 1, 2, 3]
