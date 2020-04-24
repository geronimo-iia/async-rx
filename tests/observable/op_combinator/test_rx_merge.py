from async_rx.observable import rx_range, rx_merge, rx_from
from async_rx.protocol import Observer
from async_rx.subject import subject

from ...model import ObserverCounterCollector


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
