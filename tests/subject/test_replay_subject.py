from async_rx.observable import rx_range
from async_rx.protocol import Observer
from async_rx.subject import replay_subject

from ..model import ObserverCounterCollector


def test_replay_subject(kernel):

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()

    a_subject = replay_subject(buffer_size=4)
    assert a_subject

    # first registration
    sub_a = kernel.run(a_subject.subscribe(seeker_a))
    sub_subject = kernel.run(rx_range(start=0, stop=10).subscribe(a_subject))
    assert seeker_a.on_next_count == 10
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1

    # second registration
    sub_b = kernel.run(a_subject.subscribe(seeker_b))
    assert seeker_b.on_next_count == 4  # buffer size
    assert seeker_b.on_error_count == 0
    assert seeker_b.on_completed_count == 1

    kernel.run(sub_a())
    kernel.run(sub_b())
