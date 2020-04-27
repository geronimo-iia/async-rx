import pytest
from async_rx import rx_dict

from ..model import ObserverCounterCollector

def test_rx_dict_default_dict_behaviour():
    a = rx_dict()
    assert  a == {}
    
    a["A"] = True
    a["B"] = False
    
    assert a["A"]
    assert not a["B"]
    
    assert "A" in a
    assert "B" in a
    assert "C" not in a

    del a["B"]
    assert "B" not in a

    a["A"] = 1
    assert a["A"] == 1


def test_rx_dict_with_observer_in_async_word(kernel):

    seeker = ObserverCounterCollector()


    async def _test():
        nonlocal seeker
        a = rx_dict()
        sub = await a.subscribe(seeker)
        assert seeker.on_next_count == 1
        assert seeker.items == [{}]

        a["A"] = True
        a["B"] = False

        await sub()

    kernel.run(_test())
    # there is no guarantees on notification
    assert seeker.on_next_count <= 3
    if seeker.on_next_count == 2:
        assert seeker.items == [{}, {'A': True, 'B': False}]


def test_rx_dict_on_subscription_support(kernel):
    o1 = ObserverCounterCollector()
    o2 = ObserverCounterCollector()
    a = rx_dict()
    sub_1 = kernel.run(a.subscribe(o1))

    # second cannot subscribe
    with pytest.raises(RuntimeError):
        kernel.run(a.subscribe(o2))

    # release subscription
    kernel.run(sub_1())

    # now second can subscribe
    sub_2 = kernel.run(a.subscribe(o2))
    kernel.run(sub_2())

