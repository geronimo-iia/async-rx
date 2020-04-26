from typing import Any

import pytest

from async_rx import Observer, rx_skip

from ..model import ObserverCounterCollector
from .model import get_observable


def test_rx_skip(kernel):

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_skip(observable=get_observable(), count=5).subscribe(an_observer=seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 95
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0:2] == [5, 6]

    with pytest.raises(RuntimeError):
        rx_skip(observable=get_observable(), count=0)

    with pytest.raises(RuntimeError):
        rx_skip(observable=get_observable(), count=-1)
