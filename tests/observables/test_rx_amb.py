from async_rx import Observer, rx_amb, rx_create, rx_from, rx_range

from ..model import ObserverCounterCollector
from .model import countdown


def test_rx_amb(kernel):

    seeker = ObserverCounterCollector()

    a = rx_create(subscribe=kernel.run(countdown(5, 0.1)))
    b = rx_create(subscribe=kernel.run(countdown(10, 0.2)))

    obs = rx_amb(a, b)
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())
    print(seeker.items)
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
    print(seeker.items)
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 1
    assert seeker.items == [b]
