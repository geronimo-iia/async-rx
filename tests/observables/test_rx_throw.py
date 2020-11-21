import pytest

from async_rx import Observable, Observer, rx_throw

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_rx_throw():
    obs: Observable = rx_throw(error="oulala")

    seeker = ObserverCounterCollector()

    await obs.subscribe(seeker)

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
