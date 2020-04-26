from async_rx import Observer, rx_range, rx_zip, rx_from

from ..model import ObserverCounterCollector


def test_rx_merge(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=2), rx_from("abc"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 2
    assert seeker.items == [(0, 'a'), (1, 'b')]


def test_rx_merge_b(kernel):

    seeker = ObserverCounterCollector()

    obs = rx_zip(rx_range(start=0, stop=5), rx_from("abc"))
    sub_a = kernel.run(obs.subscribe(seeker))
    kernel.run(sub_a())

    assert seeker.on_completed_count == 1
    assert seeker.on_error_count == 0
    assert seeker.on_next_count == 3
    assert seeker.items == [(0, 'a'), (1, 'b'), (2, 'c')]
