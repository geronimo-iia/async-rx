import pytest

from async_rx.protocol import default_error


@pytest.mark.curio
async def test_default_error_with_message(kernel):
    with pytest.raises(Exception):
        await default_error(err="big hup")


@pytest.mark.curio
async def test_default_error_with_Exception(kernel):
    with pytest.raises(Exception):
        await default_error(err=RuntimeError("Ouch"))
