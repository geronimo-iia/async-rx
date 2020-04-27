from typing import Any
from async_rx import rx_group_by, rx_range, rx_dict, rx_sum, rx_avg, rx_throw, rx_concat

from ..model import ObserverCounterCollector


class ObserverGroupByCollector:
    # TODO we should find something clever.

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


def test_rx_group_by(kernel):

    seeker = ObserverGroupByCollector(observer_factory=_observer_factory)

    sub = kernel.run(rx_group_by(rx_range(start=0, stop=10), _key_selector).subscribe(seeker))
    kernel.run(sub())

    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0

    (s, a) = seeker.result["odd"]
    assert s.items == [20]
    assert a.items == [4.0]

    (s, a) = seeker.result["even"]
    assert s.items == [25]
    assert a.items == [5.0]


def test_rx_group_by_with_error(kernel):
    seeker = ObserverGroupByCollector(observer_factory=_observer_factory)
    sub = kernel.run(rx_group_by(rx_concat(rx_range(start=0, stop=10), rx_throw("oups")), _key_selector).subscribe(seeker))
    kernel.run(sub())
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


def test_rx_group_by_simple(kernel):
    async def _key_selector(item: int) -> str:
        return "odd" if item % 2 == 0 else "even"

    seeker = ObserverCounterCollector()

    sub = kernel.run(rx_group_by(rx_range(start=0, stop=10), _key_selector).subscribe(seeker))
    kernel.run(sub())
    assert seeker.on_next_count == 2
    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.items[0][0] == "odd"
    assert seeker.items[1][0] == "even"
