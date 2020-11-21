import curio
import pytest

from async_rx import Observer, Subscription, rx_concat, rx_create, rx_from, rx_range, rx_repeat_series, rx_throw

from ..model import ObserverCounterCollector
from .model import countdown


@pytest.mark.curio
async def test_rx_concat_concurrent():

    seeker = ObserverCounterCollector()

    async def _build():
        return rx_concat(rx_create(subscribe=await countdown(5, 0.1)), rx_create(subscribe=await countdown(5, 0.2)))

    obs = await _build()
    sub_a = await obs.subscribe(seeker)
    await sub_a()
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 10
    assert seeker.items == [5, 4, 3, 2, 1, 5, 4, 3, 2, 1]


@pytest.mark.curio
async def test_rx_concat():

    seeker = ObserverCounterCollector()

    obs = rx_concat(rx_range(start=1, stop=20), rx_from("i am an iterable"))
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
async def test_rx_concat_with_error():
    async def sub(an_observer: Observer) -> Subscription:
        await an_observer.on_error("AA")

    seeker = ObserverCounterCollector()

    obs = rx_concat(rx_range(start=1, stop=20), rx_create(subscribe=sub))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 19


@pytest.mark.curio
async def test_rx_concat_with_throw():

    seeker = ObserverCounterCollector()

    obs = rx_concat(rx_range(start=1, stop=20), rx_throw("oups"))
    sub_a = await obs.subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1
    assert seeker.on_next_count == 19


@pytest.mark.curio
async def test_rx_concat_with_series_throw():

    seeker = ObserverCounterCollector()

    obs = rx_concat(rx_repeat_series([(0.1, "A"), (0.5, "B"), (1.0, "C")]), rx_throw("oups"))
    sub_a = await obs.subscribe(seeker)
    await curio.sleep(3)
    await sub_a()

    assert seeker.on_next_count == 3
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1


@pytest.mark.curio
async def test_rx_concat_with_no_observable():

    with pytest.raises(RuntimeError):
        rx_concat()
