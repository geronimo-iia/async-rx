import pytest

from async_rx import Observable, Observer, rx_create
from async_rx.protocol import default_subscription

from ..model import ObserverCounter


def test_rx_create_profile_test():
    with pytest.raises(RuntimeError):
        rx_create(subscribe=None)  # type: ignore


@pytest.mark.curio
async def test_rx_create_with_default():
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    obs: Observable = rx_create(subscribe=_subscribe)

    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = await obs.subscribe(seeker)
    await unsub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0


@pytest.mark.curio
async def test_rx_create_with_no_ensure_contract():
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    obs: Observable = rx_create(subscribe=_subscribe, ensure_contract=False)

    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = await obs.subscribe(seeker)
    await unsub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0


@pytest.mark.curio
async def test_rx_create_max_observer():
    async def _subscribe(an_observer: Observer):
        await an_observer.on_next(item=1)
        await an_observer.on_completed()
        return default_subscription

    obs: Observable = rx_create(subscribe=_subscribe, max_observer=1)

    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = await obs.subscribe(seeker)
    await unsub()

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0

    # ok because we had called unsub
    unsub = await obs.subscribe(seeker)

    # raise because max_observer = 1
    with pytest.raises(RuntimeError):
        unsub = await obs.subscribe(seeker)
