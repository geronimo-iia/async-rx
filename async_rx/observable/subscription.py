"""Subscription utilities."""
from typing import List

from ..protocol import Subscription

__all__ = ["default_subscription", "composite_subscription"]


async def default_subscription() -> None:
    """Do nothing."""
    pass


async def composite_subscription(subscriptions: List[Subscription]) -> Subscription:
    """Aggregate a list of subscription.

    Args:
        subscriptions (List[Subscription]): a list of subscription to aggregate

    Returns:
        (Subscription): a single subscription

    """
    is_done = False

    async def _unsubscribe() -> None:
        """Unsubscribe all subscription only once."""
        nonlocal is_done

        if not is_done:
            for s in subscriptions:
                await s()
            is_done = True

    return _unsubscribe
