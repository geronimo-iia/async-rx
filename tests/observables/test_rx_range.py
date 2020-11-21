import pytest

from async_rx import Observable, Observer, rx_range
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_rx_range():
    obs: Observable = rx_range(start=1, stop=4)

    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 3
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3]
