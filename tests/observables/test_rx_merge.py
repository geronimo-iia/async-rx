import curio
import pytest

from async_rx import Observer, Subscription, rx_create, rx_from, rx_merge, rx_range
from async_rx.protocol import default_subscription

from ..model import ObserverCounterCollector
from .model import countdown


def test_rx_merge_default():
    with pytest.raises(RuntimeError):
        rx_merge()


@pytest.mark.curio
async def test_rx_merge_concurrent():

    seeker = ObserverCounterCollector()

    async def _build():
        return rx_merge(rx_create(subscribe=await countdown(10, 0.1)), rx_create(subscribe=await countdown(10, 0.2)))

    obs = await _build()
    sub_a = await obs.subscribe(seeker)
    await sub_a()
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 20
    assert seeker.items == [10, 10, 9, 8, 9, 7, 6, 8, 5, 4, 7, 3, 2, 6, 1, 5, 4, 3, 2, 1]


@pytest.mark.curio
async def test_rx_merge():

    seeker = ObserverCounterCollector()

    obs = rx_merge(rx_range(start=1, stop=20), rx_from("i am an iterable"))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == (20 - 1 + len("i am an iterable"))
    assert seeker.items == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        "i",
        " ",
        "a",
        "m",
        " ",
        "a",
        "n",
        " ",
        "i",
        "t",
        "e",
        "r",
        "a",
        "b",
        "l",
        "e",
    ]


@pytest.mark.curio
async def test_rx_merge_with_error():

    seeker = ObserverCounterCollector()

    async def _subscribe(an_observer: Observer) -> Subscription:
        await curio.sleep(0.2)
        await an_observer.on_error(err="Args")
        return default_subscription

    async def _build():
        return rx_merge(rx_create(subscribe=await countdown(10, 0.1)), rx_create(subscribe=_subscribe))

    obs = await _build()
    sub_a = await obs.subscribe(seeker)
    await sub_a()
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count <= 3
    assert seeker.items[0] == 10
    if seeker.on_next_count > 2:
        assert seeker.items[1] == 9
