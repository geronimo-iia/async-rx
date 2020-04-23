from async_rx.observable import rx_count
from ...model import ObserverCounterCollector
from .model import get_observable


def test_rx_count(kernel):

    seeker = ObserverCounterCollector()
    sub = kernel.run(rx_count(observable=get_observable()).subscribe(seeker))
    kernel.run(sub())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [21]
