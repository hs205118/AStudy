import pytest
from app.core.state_machine import ensure_transition
from app.domain.enums import RunStatus

def test_valid_transition():
    ensure_transition(RunStatus.CREATED, RunStatus.INPUT_VALIDATING)

def test_invalid_transition():
    with pytest.raises(ValueError):
        ensure_transition(RunStatus.CREATED, RunStatus.COMPLETED)
