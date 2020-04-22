from typing import Any

import pytest

from async_rx.op_filter import rx_last
from async_rx.protocol import Observer

from ..model import ObserverCounterCollector
from .model import get_observable


def test_rx_last_with_default(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_last(observable=get_observable()).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [99]


def test_rx_last(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_last(observable=get_observable(), count=5).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 5
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == list(range(95, 100))

    with pytest.raises(RuntimeError):
        rx_last(observable=get_observable(), count=0)

    with pytest.raises(RuntimeError):
        rx_last(observable=get_observable(), count=-1)
