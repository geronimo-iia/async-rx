from ..protocol import Observable
from .rx_from import rx_from

__all__ = ["rx_of"]


def rx_of(*args) -> Observable:
    """Convert arguments into an observable sequence.

    Args:
        args: any list of argument to send to observer.

    Returns:
        (Observable): observable instance.

    """
    return rx_from(observable_input=args)
