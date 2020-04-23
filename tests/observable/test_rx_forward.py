import pytest

from async_rx.observable import rx_create, rx_forward
from async_rx.protocol import Observable, Observer, default_subscription

from ..model import ObserverCounter, ObserverCounterSilentError


async def _subscribe(an_observer: Observer):
    await an_observer.on_next(item=1)
    await an_observer.on_completed()
    return default_subscription


async def _subscribe_with_error(an_observer: Observer):
    await an_observer.on_next(item=1)
    await an_observer.on_error(err="test")
    await an_observer.on_completed()
    return default_subscription


def test_rx_forward_with_default(kernel):
    obs: Observable = rx_create(subscribe=_subscribe)

    forwarded_obs = rx_forward(observable=obs)
    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = kernel.run(forwarded_obs.subscribe(seeker))
    kernel.run(unsub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0


def test_rx_forward_without_complete(kernel):
    obs: Observable = rx_create(subscribe=_subscribe)

    forwarded_obs = rx_forward(observable=obs, except_complet=True)
    seeker = ObserverCounter()

    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    unsub = kernel.run(forwarded_obs.subscribe(seeker))
    kernel.run(unsub())

    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 0  # not forwarded
    assert seeker.on_error_count == 0


def test_rx_forward_without_error(kernel):

    seeker = ObserverCounter()
    assert seeker.on_next_count == 0
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0

    # no error because is silent
    with pytest.raises(Exception):
        kernel.run(rx_create(subscribe=_subscribe_with_error).subscribe(seeker))
    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 0  # because ensure contract enabled
    assert seeker.on_error_count == 1

    kernel.run(rx_forward(observable=rx_create(subscribe=_subscribe_with_error), except_error=True).subscribe(seeker))
    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 0  # because ensure contract enabled
    assert seeker.on_error_count == 1


def test_rx_forward_without_completed(kernel):

    seeker = ObserverCounter()

    kernel.run(rx_forward(observable=rx_create(subscribe=_subscribe), except_complet=True).subscribe(seeker))
    assert seeker.on_next_count == 1
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 0
