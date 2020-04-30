import pytest

from async_rx.protocol import observable


def test_observable_default():
    with pytest.raises(RuntimeError):
        observable(subscribe=None)
