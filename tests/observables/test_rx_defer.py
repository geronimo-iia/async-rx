import pytest

from async_rx import Observable, Observer, rx_create, rx_defer
from async_rx.protocol import default_subscription

from ..model import ObserverCounter


@pytest.mark.curio
async def test_rx_defer():
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    async def _observable_factory():
        return rx_create(subscribe=_subscribe, max_observer=1)

    obs = rx_defer(observable_factory=_observable_factory)

    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0
    unsub1 = await obs.subscribe(seeker)
    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0

    # even with max_observer=1 we can do that because of rx_defer
    unsub2 = await obs.subscribe(seeker)
    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 2
    assert seeker.on_error_count == 0
