import pytest

from async_rx import rx_count

from ..model import ObserverCounterCollector
from .model import get_observable_to_21


@pytest.mark.curio
async def test_rx_count():

    seeker = ObserverCounterCollector()
    sub = await rx_count(observable=get_observable_to_21()).subscribe(seeker)
    await sub()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [21]
