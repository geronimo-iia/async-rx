from typing import Any

import pytest

from async_rx.observable import rx_distinct, rx_from
from async_rx.protocol import Observer

from ...model import ObserverCounterCollector
from .model import get_observable


def test_rx_distinct_dummy(kernel):
    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_distinct(observable=get_observable(), frame_size=3).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 100
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0:3] == [0, 1, 2]

    with pytest.raises(RuntimeError):
        rx_distinct(observable=get_observable(), frame_size=0)

    with pytest.raises(RuntimeError):
        rx_distinct(observable=get_observable(), frame_size=-1)


def test_rx_distinct(kernel):

    source = lambda: rx_from(observable_input=[1, 2, 1, 3, 2, 1, 4, 3, 2, 1, 5, 4, 3, 2, 1])

    seeker = ObserverCounterCollector()
    sub = kernel.run(rx_distinct(observable=source(), frame_size=3).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 9
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3, 4, 1, 5, 3, 2, 1]

    seeker = ObserverCounterCollector()
    sub = kernel.run(rx_distinct(observable=source(), frame_size=2).subscribe(an_observer=seeker))
    kernel.run(sub())
    assert seeker.on_next_count == 13
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [1, 2, 3, 1, 4, 3, 2, 1, 5, 4, 3, 2, 1]
