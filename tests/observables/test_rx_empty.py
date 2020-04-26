import pytest

from async_rx import Observable, Observer, rx_empty
from async_rx.protocol import default_subscription

from ..model import ObserverCounter


def test_rx_empty(kernel):

    obs: Observable = rx_empty()

    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = kernel.run(obs.subscribe(seeker))
    kernel.run(unsub())

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
