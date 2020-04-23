from ...protocol import Observable

__all__ = ["rx_debounce"]


def rx_debounce(an_observable: Observable, time_period_seconds: float) -> Observable:
    """Emit a value from the source Observable only after a particular time.

    Time span is determined by another Observable has passed without another
    source emission.
    """
    raise RuntimeError('Not yet impleted')
