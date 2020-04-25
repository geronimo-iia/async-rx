from ...protocol import Observable

__all__ = ["rx_debounce"]


def rx_debounce(an_observable: Observable, time_period_seconds: float) -> Observable:
    """Emit a value from the source Observable only after a particular time.

    Time span is determined by another Observable has passed without another
    source emission.
    The following three operators, Debounce, Sample and Throttle are used to rate-limit the sequence.
    They will filter out elements based on the timing. There is a difference in how they exactly do that.
    Debounce will delay a value when it arrives and only emits the last value in a burst of events
    after the set delay is over and no new event arrives during this delay. 
    Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout.
    Sample will emit the latest value on a set interval or emit nothing if no new value arrived during the last interval.

    Not yet implemented !!

    """
    raise RuntimeError('Not yet implemented !!')
