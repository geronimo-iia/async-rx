from datetime import timedelta

import curio
import pytest

from async_rx import rx_concat, rx_from, rx_repeat_series, rx_sample, rx_throw

from ..model import ObserverCounterCollectorWithTime


def test_rx_sample_default():
    with pytest.raises(RuntimeError):
        rx_sample(None, None)
    with pytest.raises(RuntimeError):
        rx_sample(rx_from([1, 2]), None)
    with pytest.raises(RuntimeError):
        rx_sample(None, lambda a: not a)


@pytest.mark.curio
async def test_rx_sample():
    source = rx_sample(
        rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), duration=timedelta(seconds=0.5)
    )
    # A0:     -> 0.5
    # A1: 0.1 -> 0.6
    # A2: 0.2 -> 0.7
    # A3: 0.3 -> 0.8
    #     0.6 -> send A3
    # B:  0.8 -> 1.3
    #     1.0 ? send B
    #     1.5 ? none
    #     2.0 ? none
    # C:  1.8 -> 2.3
    #     2.5 -> send C
    #     3.0 -> none
    #     3.5 -> none
    #     4.0 -> none
    #     4.5 -> none
    # D:  4.8 -> 5.3
    #     5.0 -> none
    #     5.3 -> complete
    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.on_completed_count == 1

    assert len(seeker.items) == 3
    assert seeker.items[0][1] == "A3"
    assert seeker.items[1][1] == "B"
    assert seeker.items[2][1] == "C"
    assert seeker.get_delta() == [0.5, 1.0]  # see duration


@pytest.mark.curio
async def test_rx_sample_with_error():
    source = rx_sample(
        rx_concat(rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), rx_throw("oups")),
        duration=timedelta(seconds=0.5),
    )

    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 1
    assert seeker.on_completed_count == 0

    assert len(seeker.items) == 3
    assert seeker.items[0][1] == "A3"
    assert seeker.items[1][1] == "B"
    assert seeker.items[2][1] == "C"
    assert seeker.get_delta() == [0.5, 1.0]  # see duration
