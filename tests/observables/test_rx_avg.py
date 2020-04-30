from async_rx import Observer, Subscription, rx_avg, rx_create
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import get_observable_to_21


def test_rx_avg(kernel):

    seeker = ObserverCounterCollector()
    sub = kernel.run(rx_avg(observable=get_observable_to_21()).subscribe(seeker))
    kernel.run(sub())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [10.0]


def test_rx_avg_with_no_value_send_error(kernel):
    async def _subscription(an_observer: Observer) -> Subscription:
        await an_observer.on_completed()
        return default_subscription

    seeker = ObserverCounterCollector()
    sub = kernel.run(rx_avg(observable=rx_create(subscribe=_subscription)).subscribe(seeker))
    kernel.run(sub())

    assert seeker.on_completed_count == 0
    assert seeker.on_next_count == 0
    assert seeker.on_error_count == 1
