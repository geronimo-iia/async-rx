import pytest

from async_rx.protocol import ensure_observable_contract_operator

from ..model import ObserverCounter


def test_ensure_observable_contract_operator_nothing_is_call_after_complete(kernel):

    obs = ObserverCounter()

    enforced_observer = ensure_observable_contract_operator(obs)

    assert obs.on_next_count == 0
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    kernel.run(enforced_observer.on_next("a"))
    kernel.run(enforced_observer.on_next("a"))
    kernel.run(enforced_observer.on_next("a"))

    assert obs.on_next_count == 3
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    kernel.run(enforced_observer.on_completed())

    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0

    # next locked
    kernel.run(enforced_observer.on_next("a"))
    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0

    # on_error locked
    kernel.run(enforced_observer.on_error("ouch"))
    assert obs.on_next_count == 3
    assert obs.on_completed_count == 1
    assert obs.on_error_count == 0


def test_ensure_observable_contract_operator_nothing_is_call_after_error(kernel):

    obs = ObserverCounter()

    enforced_observer = ensure_observable_contract_operator(obs)

    assert obs.on_next_count == 0
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    kernel.run(enforced_observer.on_next("a"))
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 0

    with pytest.raises(Exception):
        kernel.run(enforced_observer.on_error("ouch"))

    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1

    kernel.run(enforced_observer.on_next("a"))
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1

    kernel.run(enforced_observer.on_completed())
    assert obs.on_next_count == 1
    assert obs.on_completed_count == 0
    assert obs.on_error_count == 1
