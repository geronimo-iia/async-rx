from collections import namedtuple
from typing import Any, TypeVar

from .definition import Collector

__all__ = ["rx_collector"]

T = TypeVar("T")

_CollectorDefinition = namedtuple("Collector", ["on_next", "on_error", "on_completed", "result", "is_finish", "has_error", "error"])


def rx_collector(initial_value: T) -> Collector:
    """Create an observer collector.

    Args:
        initial_value (T): initial value which determin result type (list, dict, base type)

    Returns:
        (Collector[T]): a collector instance

    """

    _is_finish = False
    _has_error = False
    _error = None

    if isinstance(initial_value, dict):
        _dict = dict(initial_value)

        async def _on_next(item: Any):
            nonlocal _dict
            (k, v) = item
            _dict[k] = v

        def _get_result() -> Any:
            nonlocal _dict
            return _dict

    elif isinstance(initial_value, list):
        _list = list(initial_value)

        async def _on_next(item: Any):
            nonlocal _list
            _list.append(item)

        def _get_result() -> Any:
            nonlocal _list
            return _list

    else:
        _value = initial_value

        async def _on_next(item: Any):
            nonlocal _value
            _value = item

        def _get_result() -> Any:
            nonlocal _value
            return _value

    async def _on_completed():
        nonlocal _is_finish
        _is_finish = True

    async def _on_error(err: Any):
        nonlocal _has_error, _error
        _error = err
        _has_error = True

    def _get_is_finish():
        nonlocal _is_finish
        return _is_finish

    def _get_has_error():
        nonlocal _has_error
        return _has_error

    def _get_error():
        nonlocal _error
        return _error

    return _CollectorDefinition(
        on_next=_on_next,
        on_error=_on_error,
        on_completed=_on_completed,
        result=_get_result,
        is_finish=_get_is_finish,
        has_error=_get_has_error,
        error=_get_error,
    )
