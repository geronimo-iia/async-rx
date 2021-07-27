"""Protocol test definition."""
from async_rx.protocol import Observable, Observer, Subscription, rx_observer
from async_rx.protocol.observable import ObservableDefinition


def test_rx_observer_implements_protocol():
    async def _on_next(item: str):
        pass

    obs: Observer = rx_observer(on_next=_on_next)
    assert obs


def test_observable_definition_implements_protocol():
    async def _subscribe(observer: Observer) -> Subscription:
        async def _unsub():
            pass

        return _unsub

    obs: Observable = ObservableDefinition(subscribe=_subscribe)

    assert obs
