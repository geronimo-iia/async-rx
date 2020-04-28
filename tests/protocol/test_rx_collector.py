from async_rx import rx_collector, rx_from, rx_create
from async_rx.protocol import Observer, Subscription, default_subscription


def test_rx_collector_as_hint(kernel):
    _collector = rx_collector(0)
    sub = kernel.run(rx_from([1, 2, 3, 4, 5]).subscribe(_collector))
    kernel.run(sub())
    assert _collector.result() == 5
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


def test_rx_collector_as_list(kernel):
    _collector = rx_collector([])
    sub = kernel.run(rx_from([1, 2, 3, 4, 5]).subscribe(_collector))
    kernel.run(sub())
    assert _collector.result() == [1, 2, 3, 4, 5]
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


def test_rx_collector_as_dict(kernel):
    _collector = rx_collector({})
    sub = kernel.run(rx_from([('a', 1), ('b', 2), ('c', {"sub": True})]).subscribe(_collector))
    kernel.run(sub())
    assert _collector.result() == {'a': 1, 'b': 2, 'c': {"sub": True}}
    assert _collector.is_finish()
    assert not _collector.has_error()
    assert not _collector.error()


def test_rx_collector_with_error(kernel):
    async def _subscribe(an_observer: Observer) -> Subscription:
        await an_observer.on_error("Oups")
        return default_subscription

    _collector = rx_collector({})
    sub = kernel.run(rx_create(subscribe=_subscribe).subscribe(_collector))
    kernel.run(sub())
    assert not _collector.result()
    assert not _collector.is_finish()
    assert _collector.has_error()
    assert _collector.error() == "Oups"
