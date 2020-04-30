import curio
import pytest

from async_rx import rx_list

from ..model import ObserverCounterCollector


def test_rx_list_default_behavior():

    l = rx_list()
    assert l == []

    l.append("A")
    l.append("B")
    assert l == ["A", "B"]

    l += "C"
    assert l == ["A", "B", "C"]

    l *= 2
    assert l == ["A", "B", "C", "A", "B", "C"]

    l[1] = "D"
    assert l == ["A", "D", "C", "A", "B", "C"]

    del l[2]
    assert l == ["A", "D", "A", "B", "C"]

    l += "E"
    assert l == ["A", "D", "A", "B", "C", "E"]

    l.insert(0, "Z")
    assert l == ["Z", "A", "D", "A", "B", "C", "E"]

    l.pop()
    assert l == ["Z", "A", "D", "A", "B", "C"]

    l.remove("Z")
    assert l == ["A", "D", "A", "B", "C"]

    nl = l.copy()
    assert nl == ["A", "D", "A", "B", "C"]

    l.insert(0, "Z")
    assert nl != l

    nl.clear()
    assert nl == []

    l.reverse()
    assert l == ["C", "B", "A", "D", "A", "Z"]

    l.sort()
    assert l == ["A", "A", "B", "C", "D", "Z"]

    l.extend(["AA", "BB"])
    assert l == ["A", "A", "B", "C", "D", "Z", "AA", "BB"]

    a = l + ["F"]
    assert hasattr(a, "subscribe")

    b = l * 2
    assert hasattr(b, "subscribe")


def test_rx_list_with_observer(kernel):

    seeker = ObserverCounterCollector()
    l = rx_list()
    sub = kernel.run(l.subscribe(seeker))
    assert seeker.on_next_count == 1
    assert seeker.items == [[]]

    l.append("A")
    l.append("B")
    kernel.run(curio.sleep(1))
    l += "C"
    kernel.run(curio.sleep(1))
    l *= 2
    kernel.run(curio.sleep(1))

    kernel.run(sub())
    assert l == ["A", "B", "C", "A", "B", "C"]

    # there is no guarantees on notification
    assert seeker.on_next_count <= 5
    assert seeker.items == [[], ['A', 'B'], ['A', 'B', 'C'], ['A', 'B', 'C', 'A', 'B', 'C']]


def test_rx_list_support_one_observer(kernel):

    l = rx_list()
    sub = kernel.run(l.subscribe(ObserverCounterCollector()))
    with pytest.raises(RuntimeError):
        sub = kernel.run(l.subscribe(ObserverCounterCollector()))
