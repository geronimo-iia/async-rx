import pytest

from async_rx import rx_range, rx_subject_behavior
from async_rx.protocol import Observer, subject_handler

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_replay_subject():

    current = None

    async def _on_unsub_subscribe(count: int, source: Observer):
        nonlocal current
        current = count

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()

    a_subject = rx_subject_behavior(subject_handler=subject_handler(on_subscribe=_on_unsub_subscribe, on_unsubscribe=_on_unsub_subscribe))
    assert a_subject

    # first registration
    sub_a = await a_subject.subscribe(seeker_a)
    sub_subject = await rx_range(start=0, stop=10).subscribe(a_subject)
    assert seeker_a.on_next_count == 10
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1
    assert current == 1
    # second registration
    sub_b = await a_subject.subscribe(seeker_b)
    assert seeker_b.on_next_count == 1  # buffer size
    assert seeker_b.on_error_count == 0
    assert seeker_b.on_completed_count == 1
    assert current == 2
    await sub_a()
    assert current == 1
    await sub_b()
    assert current == 0
