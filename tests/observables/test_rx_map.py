import pytest

from async_rx import rx_from, rx_map

from ..model import ObserverCounterCollector


@pytest.mark.curio
async def test_rx_map_with_async():

    seeker = ObserverCounterCollector()

    async def add(i):
        return i + 2

    sub_a = await rx_map(observable=rx_from([1, 2, 3]), transform=add).subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.items == [3, 4, 5]


@pytest.mark.curio
async def test_rx_map_sync():

    seeker = ObserverCounterCollector()

    def add(i):
        return i + 3

    sub_a = await rx_map(observable=rx_from([1, 2, 3]), transform=add).subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.items == [4, 5, 6]


@pytest.mark.curio
async def test_rx_map_with_expand_args():

    seeker = ObserverCounterCollector()

    def add(i, j):
        return i + j

    sub_a = await rx_map(observable=rx_from([(1, 2), (3, 4), (5, 6)]), transform=add, expand_arg_parameters=True).subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 3
    assert seeker.on_error_count == 0
    assert seeker.items == [3, 7, 11]


@pytest.mark.curio
async def test_rx_map_with_expand_kwargs():

    seeker = ObserverCounterCollector()

    def inc(i):
        return i + 1

    sub_a = await rx_map(observable=rx_from([{'i': 1}, {'i': 4}]), transform=inc, expand_kwarg_parameters=True).subscribe(seeker)
    await sub_a()

    assert seeker.on_completed_count == 1
    assert seeker.on_next_count == 2
    assert seeker.on_error_count == 0
    assert seeker.items == [2, 5]
