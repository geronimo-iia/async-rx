from async_rx.observable import rx_of
from async_rx.protocol import Observable, Observer

from ..model import ObserverCounterCollector


def test_rx_of(kernel):

    obs: Observable = rx_of(1, 2, 3)

    seeker = ObserverCounterCollector()

    kernel.run(obs.subscribe(seeker))

    assert seeker.on_next_count == 3
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3]
