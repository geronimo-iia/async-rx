import pytest

from async_rx import rx_collector, rx_create, rx_from
from async_rx.protocol import Observer, Subscription, default_subscription


@pytest.mark.curio
async def test_rx_collector_as_hint():
    _collector = rx_collector(0)
    sub = await rx_from([1, 2, 3, 4, 5]).subscribe(_collector)
    await sub()
    assert _collector.result() == 5
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


@pytest.mark.curio
async def test_rx_collector_as_list():
    _collector = rx_collector([])
    sub = await rx_from([1, 2, 3, 4, 5]).subscribe(_collector)
    await sub()
    assert _collector.result() == [1, 2, 3, 4, 5]
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


@pytest.mark.curio
async def test_rx_collector_as_dict():
    _collector = rx_collector({})
    sub = await rx_from([('a', 1), ('b', 2), ('c', {"sub": True})]).subscribe(_collector)
    await sub()
    assert _collector.result() == {'a': 1, 'b': 2, 'c': {"sub": True}}
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


@pytest.mark.curio
async def test_rx_collector_with_error():
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_error("Oups")
        return default_subscription

    _collector = rx_collector({})
    sub = await rx_create(subscribe=_subscribe).subscribe(_collector)
    await sub()
    assert not _collector.result()
    assert not _collector.is_finish()
    assert _collector.has_error()
    assert _collector.error() == "Oups"
