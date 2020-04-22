import pytest

from async_rx.observer import default_error


def test_default_error_with_message(kernel):
    with pytest.raises(Exception):
        kernel.run(default_error(err="big hup"))


def test_default_error_with_Exception(kernel):
    with pytest.raises(Exception):
        kernel.run(default_error(err=RuntimeError("Ouch")))
