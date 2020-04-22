from typing import Any
from async_rx.protocol import Observer
from async_rx.op_filter import rx_first

from .model import get_observable
from ..model import ObserverCounterCollector


def test_rx_first(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_first(observable=get_observable()).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [0]
