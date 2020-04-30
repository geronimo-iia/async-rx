from datetime import datetime
from typing import Any, NoReturn


class ObserverCounter:
    def __init__(self):
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.on_next_count += 1

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> NoReturn:
        self.on_error_count += 1
        raise RuntimeError(err)


class ObserverCounterSilentError:
    def __init__(self):
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.on_next_count += 1

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> None:
        self.on_error_count += 1


class ObserverCounterCollector:
    def __init__(self):
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0
        self.items: Any = list([])

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.items.append(item)
        self.on_next_count += 1

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> None:
        self.on_error_count += 1


class ObserverCounterCollectorWithTime:
    """Store itema as tuple (utc, value)."""

    def __init__(self):
        self.on_next_count = 0
        self.on_completed_count = 0
        self.on_error_count = 0
        self.items: Any = list([])

    async def on_next(self, item: Any) -> None:
        """Process item."""
        self.items.append((datetime.utcnow(), item))
        self.on_next_count += 1

    async def on_completed(self) -> None:
        """Signal completion of this observable."""
        self.on_completed_count += 1

    async def on_error(self, err: Any) -> None:
        self.on_error_count += 1

    def get_delta(self):
        if len(self.items) <= 1:
            return []
        return [round((self.items[i][0] - self.items[i - 1][0]).total_seconds(), ndigits=1) for i in range(1, len(self.items))]
