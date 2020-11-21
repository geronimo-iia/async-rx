from datetime import timedelta

import curio
import pytest

from async_rx import rx_concat, rx_debounce, rx_from, rx_repeat_series, rx_throw

from ..model import ObserverCounterCollectorWithTime


def test_rx_debounce_default():
    with pytest.raises(RuntimeError):
        rx_debounce(None, None)
    with pytest.raises(RuntimeError):
        rx_debounce(rx_from([1, 2]), None)
    with pytest.raises(RuntimeError):
        rx_debounce(None, timedelta(seconds=1))


@pytest.mark.curio
async def test_rx_debounce():

    source = rx_debounce(
        rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), duration=timedelta(seconds=0.5)
    )
    # A0:     -> 0.5
    # A1: 0.1 -> 0.6
    # A2: 0.2 -> 0.7
    # A3: 0.3 -> 0.8
    #     0.5 ? old(A3) = 0.2, wake up 1.0
    # B:  0.8 -> 1.3
    #     1.0 ? old(B) = 0.2, wake up 1.5
    #     1.5 ? old(B) = 0.7 -> send, wake ip 2.0
    #     2.0 ? none, wake up 2.5
    # C:  1.8 -> 2.3
    #     2.5 -> old(C) = 0.2, wake up 3.0
    #     3.0 -> olf(C) = 0.7, send, wakup 3.5
    #     3.5 -> none, wake up 4.0
    #     4.0 -> none, wake up 4.5
    #     4.5 -> none, wake up 5.0
    # D:  4.8 -> 5.3
    #     5.0 -> none, wake up 5.5
    #     5.3 -> complete
    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()
    assert seeker.on_next_count == 2
    assert seeker.on_error_count == 0
    assert seeker.on_completed_count == 1

    assert len(seeker.items) == 2
    assert seeker.items[0][1] == "B"
    assert seeker.items[1][1] == "C"
    assert seeker.get_delta() == [1.0]


@pytest.mark.curio
async def test_rx_debounce_with_error():

    source = rx_debounce(
        rx_concat(rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), rx_throw("oups")),
        duration=timedelta(seconds=0.5),
    )

    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()

    assert len(seeker.items) == 2
    assert seeker.get_delta() == [1.0]
    assert seeker.on_next_count == 2
    assert seeker.on_error_count == 1
    assert seeker.on_completed_count == 0
