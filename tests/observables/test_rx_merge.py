
from async_rx import Observer, rx_range, rx_merge, rx_from, rx_create
from async_rx.protocol import default_subscription
from ..model import ObserverCounterCollector
from .model import countdown

def test_rx_merge_concurrent(kernel):

    seeker = ObserverCounterCollector()

    async def _build():
        return rx_merge(rx_create(subscribe=await countdown(10, 0.1)), rx_create(subscribe=await countdown(10, 0.2)))

    obs = kernel.run(_build())
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 20
    assert seeker.items == [10, 10, 9, 8, 9, 7, 6, 8, 5, 4, 7, 3, 2, 6, 1, 5, 4, 3, 2, 1]


def test_rx_merge(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_merge(rx_range(start=1, stop=20), rx_from("i am an iterable"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

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
