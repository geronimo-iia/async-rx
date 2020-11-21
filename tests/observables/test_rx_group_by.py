from typing import Any

import pytest

from async_rx import rx_avg, rx_collector, rx_concat, rx_dict, rx_group_by, rx_range, rx_subject, rx_subject_from, rx_sum, rx_throw

from ..model import ObserverCounterCollector


class ObserverGroupByCollector:
    # TODO we should find something clever ?
    #  - something like an rx_group_by_collector with an aggregate function (sum, avg, min, max, count)
    #  - something like rx_group_by_map with an observable_factory and rx_collector

    def __init__(self, observer_factory: callable):
        self.observer_factory = observer_factory
        self.result = rx_dict()
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.on_next_count += 1
        (key, obs) = item
        self.result[key] = await self.observer_factory(key, obs)

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> None:
        self.on_error_count += 1


async def _key_selector(item: int) -> str:
    return "odd" if item % 2 == 0 else "even"


async def _observer_factory(key, obs):
    _sum = ObserverCounterCollector()
    _avg = ObserverCounterCollector()
    await rx_sum(observable=obs).subscribe(_sum)
    await rx_avg(observable=obs).subscribe(_avg)
    return _sum, _avg


@pytest.mark.curio
async def test_rx_group_by():

    seeker = ObserverGroupByCollector(observer_factory=_observer_factory)

    sub = await rx_group_by(rx_range(start=0, stop=10), _key_selector).subscribe(seeker)
    await sub()

    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0

    (s, a) = seeker.result["odd"]
    assert s.items == [20]
    assert a.items == [4.0]

    (s, a) = seeker.result["even"]
    assert s.items == [25]
    assert a.items == [5.0]


@pytest.mark.curio
async def test_rx_group_by_with_error():
    seeker = ObserverGroupByCollector(observer_factory=_observer_factory)
    sub = await rx_group_by(rx_concat(rx_range(start=0, stop=10), rx_throw("oups")), _key_selector).subscribe(seeker)
    await sub()
    print(seeker.result)
    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 0
    assert seeker.on_error_count == 1

    (s, a) = seeker.result["odd"]
    assert s.on_error_count == 1
    assert a.on_error_count == 1

    (s, a) = seeker.result["even"]
    assert s.on_error_count == 1
    assert a.on_error_count == 1


@pytest.mark.curio
async def test_rx_group_by_simple():
    async def _key_selector(item: int) -> str:
        return "odd" if item % 2 == 0 else "even"

    seeker = ObserverCounterCollector()

    sub = await rx_group_by(rx_range(start=0, stop=10), _key_selector).subscribe(seeker)
    await sub()
    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0][0] == "odd"
    assert seeker.items[1][0] == "even"


@pytest.mark.curio
async def test_rx_group_by_with_collector():
    async def _observer_factory(key, obs):
        _sum = rx_collector(0)
        _avg = rx_collector(0.0)
        await rx_sum(observable=obs).subscribe(_sum)
        await rx_avg(observable=obs).subscribe(_avg)
        return {"sum": _sum, "avg": _avg}

    seeker = ObserverGroupByCollector(observer_factory=_observer_factory)

    sub = await rx_group_by(rx_range(start=0, stop=10), _key_selector).subscribe(seeker)
    await sub()

    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0

    result = {}
    for k, v in seeker.result.items():
        result[k] = {}
        for k1, v1 in v.items():
            result[k][k1] = v1.result() if v1.is_finish() else None
    assert result == {'odd': {'sum': 20, 'avg': 4.0}, 'even': {'sum': 25, 'avg': 5.0}}


@pytest.mark.curio
async def test_rx_group_by_with_subject():

    _accumulator = {}
    _subject = rx_subject()

    async def _on_next(item: Any):
        nonlocal _accumulator
        (key, an_observable) = item
        _sum = rx_collector(0)
        _avg = rx_collector(0.0)
        await rx_sum(observable=an_observable).subscribe(_sum)
        await rx_avg(observable=an_observable).subscribe(_avg)
        _accumulator[key] = {"sum": _sum, "avg": _avg}

    async def _on_complete():
        nonlocal _accumulator
        result = {}
        for k, v in _accumulator.items():
            result[k] = {}
            for k1, v1 in v.items():
                result[k][k1] = v1.result() if v1.is_finish() else None
        await _subject.on_next(item=result)
        await _subject.on_completed()

    head_subject = rx_subject_from(a_subject=_subject, on_next=_on_next, on_completed=_on_complete)

    source = rx_group_by(rx_range(start=0, stop=10), _key_selector)
    seeker = ObserverCounterCollector()

    await _subject.subscribe(seeker)
    await source.subscribe(head_subject)

    assert seeker.items == [{'odd': {'sum': 20, 'avg': 4.0}, 'even': {'sum': 25, 'avg': 5.0}}]
