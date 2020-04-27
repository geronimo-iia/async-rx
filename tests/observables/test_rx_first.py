from typing import Any

from async_rx import Observer, rx_first, rx_from

from ..model import ObserverCounterCollector
from .model import get_observable


def test_rx_first(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_first(observable=get_observable()).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == [0]


def test_rx_first_with_just_one(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_first(observable=rx_from("A")).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items == ["A"]
