import pytest

from ..model import ObserverCounter
from async_rx.protocol import Observer, Observable
from async_rx.observable import rx_empty, default_subscription


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
