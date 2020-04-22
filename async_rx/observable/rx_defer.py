from ..protocol import Observable, ObservableFactory, Observer, Subscription
from .rx_create import rx_create

__all__ = ["rx_defer"]


def rx_defer(observable_factory: ObservableFactory) -> Observable:
    """Create an observable when a subscription occurs.

    Defer allows you to create the Observable only when the Observer subscribes,
    and create a fresh Observable for each Observer.

    It waits until an Observer subscribes to it, and then it generates an Observable,
    typically with an Observable factory function.
    It does this afresh for each subscriber, so although each subscriber may think
    it is subscribing to the same Observable,
    in fact each subscriber gets its own individual Observable.

    Args:
        observable_factory (ObservableFactory): observable factory

    Returns:
        (Observable): an observable instance wich create observable
            when subscription occurs.

    """

    async def _subscribe(an_observer: Observer) -> Subscription:
        _obs = await observable_factory()
        return await _obs.subscribe(an_observer)

    return rx_create(subscribe=_subscribe)
