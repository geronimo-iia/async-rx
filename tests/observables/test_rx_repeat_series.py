import curio
import pytest

from async_rx import rx_repeat_series

from ..model import ObserverCounterCollectorWithTime


def test_rx_repeat_series_default():
    with pytest.raises(RuntimeError):
        rx_repeat_series(None)

    with pytest.raises(RuntimeError):
        rx_repeat_series(True)


def test_rx_repeat_series(kernel):

    source = rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")])

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(3))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [0.5, 1.0]


def test_rx_repeat_series_async(kernel):
    async def build():
        async def generate():  # this is an asyn generator
            for t in [(0.1, "A"), (0.5, "B"), (1.0, "C")]:
                yield t

        return rx_repeat_series(generate())

    source = kernel.run(build())

    seeker = ObserverCounterCollectorWithTime()

    sub = kernel.run(source.subscribe(seeker))
    kernel.run(curio.sleep(3))
    kernel.run(sub())

    assert len(seeker.items) == 3
    assert seeker.get_delta() == [0.5, 1.0]
