from async_rx.multicast import publish_behavior
from async_rx.observable import rx_range
from async_rx.protocol import Observer
from async_rx.subject import subject

from ..model import ObserverCounterCollector


def test_publish_behavior(kernel):

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()

    a_multicast = publish_behavior(an_observable=rx_range(start=0, stop=100))
    assert a_multicast

    # subscribe
    sub_a = kernel.run(a_multicast.subscribe(seeker_a))
    sub_b = kernel.run(a_multicast.subscribe(seeker_b))

    kernel.run(a_multicast.connect())

    # both observer see the same things
    assert seeker_a.on_next_count == seeker_b.on_next_count
    assert seeker_a.on_error_count == seeker_b.on_error_count
    assert seeker_a.on_completed_count == seeker_b.on_completed_count

    assert seeker_a.on_next_count == 100
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1

    # replay
    seeker_c = ObserverCounterCollector()
    sub_c = kernel.run(a_multicast.subscribe(seeker_c))
    assert seeker_c.on_next_count == 1
    assert seeker_c.on_error_count == 0
    assert seeker_c.on_completed_count == 1
