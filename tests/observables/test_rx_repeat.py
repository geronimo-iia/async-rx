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


def test_rx_repeat(kernel):

    seeker = ObserverCounterCollectorWithTime()
    sub = kernel.run(rx_repeat(duration=timedelta(seconds=0.2), producer=lambda: True).subscribe(seeker))
    kernel.run(curio.sleep(1.1))
    kernel.run(sub())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 6
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2, 0.2, 0.2]


def test_rx_repeat_async(kernel):
    async def _producer():
        return True

    seeker = ObserverCounterCollectorWithTime()
    sub = kernel.run(rx_repeat(duration=timedelta(seconds=0.2), producer=_producer).subscribe(seeker))
    kernel.run(curio.sleep(1.1))
    kernel.run(sub())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 6
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2, 0.2, 0.2]


def test_rx_repeat_with_initial_delay(kernel):

    seeker = ObserverCounterCollectorWithTime()
    sub = kernel.run(rx_repeat(duration=timedelta(seconds=0.2), producer=lambda: True, initial_delay=timedelta(seconds=0.4)).subscribe(seeker))
    kernel.run(curio.sleep(1.1))
    kernel.run(sub())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 4
    assert seeker.on_error_count == 0
    assert seeker.get_delta() == [0.2, 0.2, 0.2]
