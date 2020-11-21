import pytest

from async_rx.protocol import ensure_observable_contract_operator

from ..model import ObserverCounter


@pytest.mark.curio
async def test_ensure_observable_contract_operator_nothing_is_call_after_complete():

    obs = ObserverCounter()

    enforced_observer = ensure_observable_contract_operator(obs)

    assert obs.on_next_count == 0
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    await enforced_observer.on_next("a")
    await enforced_observer.on_next("a")
    await enforced_observer.on_next("a")

    assert obs.on_next_count == 3
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    await enforced_observer.on_completed()

    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0

    # next locked
    await enforced_observer.on_next("a")
    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0

    # on_error locked
    await enforced_observer.on_error("ouch")
    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0


@pytest.mark.curio
async def test_ensure_observable_contract_operator_nothing_is_call_after_error():

    obs = ObserverCounter()

    enforced_observer = ensure_observable_contract_operator(obs)

    assert obs.on_next_count == 0
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    await enforced_observer.on_next("a")
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    with pytest.raises(Exception):
        await enforced_observer.on_error("ouch")

    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1

    await enforced_observer.on_next("a")
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1

    await enforced_observer.on_completed()
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1
