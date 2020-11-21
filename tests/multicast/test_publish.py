import pytest

from async_rx import Observer, rx_publish, rx_range, rx_subject

from ..model import ObserverCounterCollector


class ConnectableObservableCounter:
    def __init__(self):
        self.connected = False

    async def on_connect(self) -> None:
        self.connected = True

    async def on_disconnect(self) -> None:
        self.connected = False


class SubjectHandlerCounter:
    def __init__(self):
        self.on_subscribe_count = 0
        self.on_unsubscribe_count = 0
        self.current = None

    async def on_subscribe(self, count: int, source: Observer) -> None:
        self.on_subscribe_count += 1
        self.current = count

    async def on_unsubscribe(self, count: int, source: Observer) -> None:
        self.on_unsubscribe_count += 1
        self.current = count


@pytest.mark.curio
async def test_multicast():

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()
    subject_handler = SubjectHandlerCounter()
    connection_handler = ConnectableObservableCounter()

    a_multicast = rx_publish(an_observable=rx_range(start=0, stop=100), subject_handler=subject_handler, connection_handler=connection_handler)
    assert a_multicast
    assert not connection_handler.connected

    # subscribe
    sub_a = await a_multicast.subscribe(seeker_a)
    assert subject_handler.on_subscribe_count == 1
    assert subject_handler.current == 1
    assert not connection_handler.connected

    sub_b = await a_multicast.subscribe(seeker_b)
    assert subject_handler.on_subscribe_count == 2
    assert subject_handler.current == 2
    assert not connection_handler.connected

    await a_multicast.connect()
    assert connection_handler.connected  # with no ref_count, did not connect automatically

    # two call on connect did not matter
    await a_multicast.connect()
    assert connection_handler.connected  # with no ref_count, did not connect automatically

    # both observer see the same things
    assert seeker_a.on_next_count == seeker_b.on_next_count
    assert seeker_a.on_error_count == seeker_b.on_error_count
    assert seeker_a.on_completed_count == seeker_b.on_completed_count

    assert seeker_a.on_next_count == 100
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1


@pytest.mark.curio
async def test_multicast_with_ref_count():

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()
    subject_handler = SubjectHandlerCounter()
    connection_handler = ConnectableObservableCounter()

    a_multicast = await rx_publish(
        an_observable=rx_range(start=0, stop=100), subject_handler=subject_handler, connection_handler=connection_handler
    ).ref_count()

    assert a_multicast
    assert not connection_handler.connected

    # subscribe
    sub_a = await a_multicast.subscribe(seeker_a)
    assert subject_handler.on_subscribe_count == 1
    assert subject_handler.current == 1

    assert connection_handler.connected  # autoconnect

    assert seeker_a.on_next_count == 100
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1

    await sub_a()
    assert not connection_handler.connected  # auto disconnect


@pytest.mark.curio
async def test_multicast_with_ref_count_on_subject():

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()
    subject_handler = SubjectHandlerCounter()
    connection_handler = ConnectableObservableCounter()

    a_subject = rx_subject()

    a_multicast = await rx_publish(an_observable=a_subject, subject_handler=subject_handler, connection_handler=connection_handler).ref_count()
    assert a_multicast
    assert not connection_handler.connected

    # subscribe
    sub_a = await a_multicast.subscribe(seeker_a)
    assert subject_handler.on_subscribe_count == 1
    assert subject_handler.current == 1

    assert connection_handler.connected  # autoconnect
    # no item in subject
    assert seeker_a.on_next_count == 0
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 0

    await a_subject.on_next(item="one")  # send "one" item
    assert seeker_a.on_next_count == 1
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 0

    await a_subject.on_next(item="two")  # send "two" item
    assert seeker_a.on_next_count == 2
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 0

    await a_subject.on_error(err="oups")  # send error
    assert seeker_a.on_next_count == 2
    assert seeker_a.on_error_count == 1
    assert seeker_a.on_completed_count == 0

    await a_subject.on_completed()  # ensure contract
    assert seeker_a.on_next_count == 2
    assert seeker_a.on_error_count == 1
    assert seeker_a.on_completed_count == 0

    await sub_a()
    assert not connection_handler.connected  # auto disconnect
