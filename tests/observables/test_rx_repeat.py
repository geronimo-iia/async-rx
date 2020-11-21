from datetime import timedelta

import curio
import pytest

from async_rx import rx_concat, rx_from, rx_repeat, rx_repeat_series, rx_throw

from ..model import ObserverCounterCollectorWithTime


def test_rx_repeat_default():
    with pytest.raises(RuntimeError):
        rx_repeat(None, None)
    with pytest.raises(RuntimeError):
        rx_repeat(rx_from([1, 2]), None)
    with pytest.raises(RuntimeError):
        rx_repeat(None, lambda a: not a)


@pytest.mark.curio
async def test_rx_repeat():

    seeker = ObserverCounterCollectorWithTime()
    sub = await rx_repeat(duration=timedelta(seconds=0.2), producer=lambda: True).subscribe(seeker)
    await curio.sleep(1.1)
    await sub()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 6
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2, 0.2, 0.2]


@pytest.mark.curio
async def test_rx_repeat_async():
    async def _producer():
        return True

    seeker = ObserverCounterCollectorWithTime()
    sub = await rx_repeat(duration=timedelta(seconds=0.2), producer=_producer).subscribe(seeker)
    await curio.sleep(1.1)
    await sub()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 6
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2, 0.2, 0.2]


@pytest.mark.curio
async def test_rx_repeat_with_initial_delay():

    seeker = ObserverCounterCollectorWithTime()
    sub = await rx_repeat(duration=timedelta(seconds=0.2), producer=lambda: True, initial_delay=timedelta(seconds=0.4)).subscribe(seeker)
    await curio.sleep(1.1)
    await sub()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 4
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2]
