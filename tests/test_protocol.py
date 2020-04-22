"""Protocol test definition."""
from async_rx.observer import observer
from async_rx.protocol import Observable, ObservableDefinition, Observer, ObserverDefinition, Subscription


def test_observer_definition_implements_protocol():
    async def _on_next(item: str):
        pass

    obs: Observer = observer(on_next=_on_next)
    assert obs


def test_observable_definition_implements_protocol():
    async def _subscribe(observer: Observer) -> Subscription:
        async def _unsub():
            pass

        return _unsub

    obs: Observable = ObservableDefinition(subscribe=_subscribe)

    assert obs
