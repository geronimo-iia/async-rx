from datetime import timedelta

import curio
import pytest

from async_rx import rx_concat, rx_from, rx_repeat_series, rx_throttle, rx_throw

from ..model import ObserverCounterCollectorWithTime


def test_rx_throttle_default():
    with pytest.raises(RuntimeError):
        rx_throttle(None, None)
    with pytest.raises(RuntimeError):
        rx_throttle(rx_from([1, 2]), None)
    with pytest.raises(RuntimeError):
        rx_throttle(None, lambda a: not a)


@pytest.mark.curio
async def test_rx_throttle():
    source = rx_throttle(
        rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), duration=timedelta(seconds=0.5)
    )
    # A0:     -> send A0, min 0.5
    # A1: 0.1
    # A2: 0.2
    # A3: 0.3
    # B:  0.8 -> send B, min 1.3
    # C:  1.8 -> send C, min 2.3
    # D:  4.8 -> send D, min, 5.3
    #     5.0 -> none
    #     5.3 -> complete
    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()
    assert seeker.on_next_count == 4
    assert seeker.on_error_count == 0
    assert seeker.on_completed_count == 1

    assert len(seeker.items) == 4
    assert seeker.items[0][1] == "A0"
    assert seeker.items[1][1] == "B"
    assert seeker.items[2][1] == "C"
    assert seeker.items[3][1] == "D"
    assert seeker.get_delta() == [0.8, 1.0, 3.0]  # see duration


@pytest.mark.curio
async def test_rx_throttle_with_error():
    source = rx_throttle(
        rx_concat(rx_repeat_series([(0.1, "A0"), (0.1, "A1"), (0.1, "A2"), (0.1, "A3"), (0.5, "B"), (1.0, "C"), (3.0, "D")]), rx_throw("oups")),
        duration=timedelta(seconds=0.5),
    )

    seeker = ObserverCounterCollectorWithTime()

    sub = await source.subscribe(seeker)
    await curio.sleep(6)
    await sub()
    assert seeker.on_next_count == 4
    assert seeker.on_error_count == 1
    assert seeker.on_completed_count == 0

    assert len(seeker.items) == 4
    assert seeker.items[0][1] == "A0"
    assert seeker.items[1][1] == "B"
    assert seeker.items[2][1] == "C"
    assert seeker.items[3][1] == "D"
    assert seeker.get_delta() == [0.8, 1.0, 3.0]  # see duration
