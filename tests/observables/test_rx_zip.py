from async_rx import Observer, Subscription, rx_create, rx_from, rx_range, rx_zip
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


def test_rx_zip_equals(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=3), rx_from("abc"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [(0, 'a'), (1, 'b'), (2, 'c')]


def test_rx_zip_limit_left(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=2), rx_from("abc"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 2
    assert seeker.items == [(0, 'a'), (1, 'b')]


def test_rx_zip_limit_right(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=5), rx_from("abc"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [(0, 'a'), (1, 'b'), (2, 'c')]


def test_rx_zip_with_error(kernel):
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_next("a")
        await an_observer.on_error("Oups")
        return default_subscription

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=3), rx_create(subscribe=_subscribe))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 1
    assert seeker.items == [(0, 'a')]
