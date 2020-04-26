from async_rx import Observer, rx_publish_replay, rx_range, rx_subject

from ..model import ObserverCounterCollector


def test_publish_replay(kernel):

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()

    a_multicast = rx_publish_replay(an_observable=rx_range(start=0, stop=100), buffer_size=3)
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
    assert seeker_c.on_next_count == 3
    assert seeker_c.on_error_count == 0
    assert seeker_c.on_completed_count == 1
