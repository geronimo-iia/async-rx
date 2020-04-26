from async_rx import rx_map, rx_from
from ..model import ObserverCounterCollector


def test_rx_map_with_async(kernel):

    seeker = ObserverCounterCollector()

    async def add(i):
        return i + 2

    sub_a = kernel.run(rx_map(observable=rx_from([1, 2, 3]), transform=add).subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.items == [3, 4, 5]


def test_rx_map_sync(kernel):

    seeker = ObserverCounterCollector()

    def add(i):
        return i + 3

    sub_a = kernel.run(rx_map(observable=rx_from([1, 2, 3]), transform=add).subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.items == [4, 5, 6]
