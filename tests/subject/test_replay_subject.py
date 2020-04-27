import pytest
from async_rx import Observer, rx_range, rx_subject_replay, Subscription, rx_create
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


def test_replay_subject_default():
    with pytest.raises(RuntimeError):
        rx_subject_replay(0)
    with pytest.raises(RuntimeError):
        rx_subject_replay(-1)


def test_replay_subject(kernel):

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()

    a_subject = rx_subject_replay(buffer_size=4)
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


def test_replay_subject_with_error(kernel):
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_next("A")
        await an_observer.on_error("Args")
        return default_subscription

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()
    a_subject = rx_subject_replay(buffer_size=4)

    sub_a = kernel.run(a_subject.subscribe(seeker_a))

    sub_subject = kernel.run(rx_create(subscribe=_subscribe).subscribe(a_subject))

    assert seeker_a.on_next_count == 1
    assert seeker_a.on_error_count == 1
    assert seeker_a.on_completed_count == 0
    assert seeker_a.items == ["A"]

    sub_b = kernel.run(a_subject.subscribe(seeker_b))
    assert seeker_b.on_next_count == 1
    assert seeker_b.on_error_count == 1
    assert seeker_b.on_completed_count == 0
    assert seeker_b.items == ["A"]

    kernel.run(sub_a())
    kernel.run(sub_b())
