import pytest
from async_rx import rx_window, rx_from, rx_empty, rx_range, Observer, Subscription, rx_create
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


def test_rx_window_default():
    with pytest.raises(RuntimeError):
        rx_window(observable=rx_empty(), buffer_size=0)
    with pytest.raises(RuntimeError):
        rx_window(observable=rx_empty(), buffer_size=-1)


def test_rx_window(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_window(rx_range(start=1, stop=20), buffer_size=5)
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    for item in seeker.items:
        assert hasattr(item, "subscribe")


def test_rx_window_with_error(kernel):
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_next(1)
        await an_observer.on_next(2)
        await an_observer.on_next(3)
        await an_observer.on_next(4)
        await an_observer.on_next(5)
        await an_observer.on_error("oups")
        return default_subscription

    seeker = ObserverCounterCollector()

    obs = rx_window(rx_create(subscribe=_subscribe), buffer_size=2)
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 2
    for item in seeker.items:
        assert hasattr(item, "subscribe")
