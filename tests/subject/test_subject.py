from async_rx.protocol import Observer
from async_rx.observable import rx_range
from async_rx.subject import subject
from ..model import ObserverCounterCollector


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


def test_subject(kernel):

    seeker_a = ObserverCounterCollector()
    seeker_b = ObserverCounterCollector()
    subject_handler = SubjectHandlerCounter()

    a_subject = subject(subject_handler=subject_handler)
    assert a_subject

    sub_a = kernel.run(a_subject.subscribe(seeker_a))
    assert subject_handler.on_subscribe_count == 1
    assert subject_handler.current == 1

    sub_b = kernel.run(a_subject.subscribe(seeker_b))
    assert subject_handler.on_subscribe_count == 2
    assert subject_handler.current == 2

    sub_subject = kernel.run(rx_range(start=0, stop=10).subscribe(a_subject))

    # both observer see the same things
    assert seeker_a.on_next_count == seeker_b.on_next_count
    assert seeker_a.on_error_count == seeker_b.on_error_count
    assert seeker_a.on_completed_count == seeker_b.on_completed_count

    assert seeker_a.on_next_count == 10
    assert seeker_a.on_error_count == 0
    assert seeker_a.on_completed_count == 1

    kernel.run(sub_a())
    assert subject_handler.on_unsubscribe_count == 1
    assert subject_handler.current == 1
    # sub are one shot
    kernel.run(sub_a())
    assert subject_handler.on_unsubscribe_count == 1
    assert subject_handler.current == 1

    kernel.run(sub_b())
    assert subject_handler.on_unsubscribe_count == 2
    assert subject_handler.current == 0
