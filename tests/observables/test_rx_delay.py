import curio
import pytest
from async_rx import rx_delay, rx_repeat_series, rx_from, rx_concat, rx_throw
from datetime import timedelta
from ..model import ObserverCounterCollectorWithTime


def test_rx_delay_default():
    with pytest.raises(RuntimeError):
        rx_delay(None, duration=None)

    with pytest.raises(RuntimeError):
        rx_delay(rx_from([1, 2]), duration=None)

    with pytest.raises(RuntimeError):
        rx_delay(rx_from([1, 2]), duration=timedelta(seconds=0.5), buffer_size=-1)


def test_rx_delay(kernel):

    source = rx_delay(rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")]), duration=timedelta(seconds=0.5), buffer_size=5)

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(3))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [0.5, 1.0]  # same interval all >= 0.5


def test_rx_delay_with_error_should_delay_error(kernel):

    source = rx_delay(rx_concat(rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")]), rx_throw("oups")), duration=timedelta(seconds=0.5))

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(3))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [0.5, 1.0]  # same interval all >= 0.5
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 1
    assert seeker.on_completed_count == 0


def test_rx_delay_minimal_interval(kernel):

    source = rx_delay(rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")]), duration=timedelta(seconds=0.5))

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(3))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [0.5, 1.0]  # same interval because duration = 0.5

    # with a longer delay
    source = rx_delay(rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")]), duration=timedelta(seconds=1.5))

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(5))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [1.5, 1.5]  # minimal duration is 1.5


def test_rx_delay_overload_buffer(kernel):

    _list = [(0.1, "A"), (0.1, "B"), (0.1, "C")] * 2
    assert len(_list) == 6

    source = rx_delay(rx_repeat_series(_list), duration=timedelta(seconds=1.5), buffer_size=2, ignore_events_if_full=True)
    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(10))
    kernel.run(sub())

    # rx_repeat_series => O.6 second,
    # A, B, C because buffer size = 2, other are ignored
    # not only A and B, because B,C arrive when A is consumed (so queue size is 0)
    assert len(seeker.items) == 3
    assert seeker.get_delta() == [1.5, 1.5]  # same interval because duration = 0.5
