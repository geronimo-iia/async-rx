import curio
import pytest
from async_rx import Observer, rx_amb, rx_create, rx_from, rx_range, Subscription
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import countdown


def test_rx_amb_init():
    with pytest.raises(RuntimeError):
        rx_amb()


def test_rx_amb(kernel):

    seeker = ObserverCounterCollector()

    a = rx_create(subscribe=kernel.run(countdown(5, 0.1)))
    b = rx_create(subscribe=kernel.run(countdown(10, 0.2)))

    obs = rx_amb(a, b)
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [a]


def test_rx_amb2(kernel):

    seeker = ObserverCounterCollector()

    a = rx_create(subscribe=kernel.run(countdown(5, 0.1)))
    b = rx_create(subscribe=kernel.run(countdown(10, 0.05)))

    obs = rx_amb(a, b)
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [b]


def test_rx_amb_with_error(kernel):

    seeker = ObserverCounterCollector()

    async def _subscribe(an_observer: Observer) -> Subscription:
        await curio.sleep(0.05)
        await an_observer.on_error(err="Args")
        return default_subscription

    a = rx_create(subscribe=kernel.run(countdown(5, 0.1)))

    obs = rx_amb(a, rx_create(subscribe=_subscribe))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [a]
