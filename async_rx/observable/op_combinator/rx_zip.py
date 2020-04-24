from typing import Any, List, NoReturn, Optional

from ...observer import observer
from ...protocol import CompleteHandler, NextHandler, Observable, Observer, Subscription
from ..rx_create import rx_create

__all__ = ["rx_zip"]


def rx_zip(*observables: Observable) -> Observable:
    """Combine multiple Observables to create an Observable.

    The Obsevable values are calculated from the values, in order,
    of each of its input Observables.

    Args:
        (Observable): a list of observable instance

    Returns:
        (Observable): observable instance

    """

    async def _subscribe(an_observer: Observer) -> Subscription:

        subscriptions: List[Subscription] = []
        sources = list(observables)
        n = len(sources)
        queues: List[List] = [[] for _ in range(n)]
        _disposable = True  # error or completed not send
        _is_done = [False] * n

        async def _subscription_handler() -> None:
            nonlocal subscriptions
            for s in subscriptions:
                await s()

        def _on_completed(i: int) -> CompleteHandler:
            async def __on_completed():
                nonlocal _disposable, _is_done
                _is_done[i] = True
                if _disposable and all(_is_done):
                    await an_observer.on_completed()
                    _disposable = False

            return __on_completed

        async def _on_error(err: Any) -> Optional[NoReturn]:
            nonlocal _disposable
            _disposable = False
            return await an_observer.on_error(err=err)

        async def _on_next_tuple(i: int) -> None:
            nonlocal _disposable, queues, _is_done

            if all(len(q) for q in queues):
                try:
                    queued_values = [x.pop(0) for x in queues]
                    await an_observer.on_next(item=tuple(queued_values))
                except Exception as ex:
                    await _on_error(ex)
            elif all(x for j, x in enumerate(_is_done) if j != i):
                _disposable = False
                await an_observer.on_completed()

        def _on_next(i: int) -> NextHandler:
            async def __on_next(item: Any) -> None:
                nonlocal _disposable, queues
                if _disposable:
                    queues[i].append(item)
                    await _on_next_tuple(i)

            return __on_next

        # observer factory
        def _observer_factory(i: int) -> Observer:
            return observer(on_next=_on_next(i), on_completed=_on_completed(i), on_error=_on_error)

        subscriptions = [await an_observable.subscribe(_observer_factory(i)) for i, an_observable in enumerate(sources)]

        return _subscription_handler

    return rx_create(subscribe=_subscribe, max_observer=1)
