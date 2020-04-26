import curio
from async_rx import rx_range, Observer
from async_rx.protocol import default_subscription


def get_observable():
    return rx_range(start=0, stop=100)


def get_observable_to_21():
    return rx_range(start=0, stop=21)


async def countdown(n, delay=1):
    async def _subscribe(an_observer: Observer):
        nonlocal n, delay
        await curio.sleep(delay)
        while n > 0:
            await an_observer.on_next(item=n)
            await curio.sleep(delay)
            n -= 1
        await an_observer.on_completed()
        return default_subscription

    return _subscribe
