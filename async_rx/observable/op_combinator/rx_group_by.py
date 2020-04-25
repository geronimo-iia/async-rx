"""

"""


from ...protocol import Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_group_by"]


def rx_group_by(*observables: Observable) -> Observable:
    """Group by operator.

    Similar to Window, GroupBy projects the sequence onto a number of inner observables
    but as opposite to Window where all windows receive the same sequence,
    GroupBy will emit elements only to one inner observable that is associated
    with the current element based on a key selector function.

    Args:
        observables (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        pass

    return rx_create(subscribe=_subscribe, max_observer=1)
