from app.domain.enums import RunStatus

_ALLOWED = {
    RunStatus.CREATED: {RunStatus.INPUT_VALIDATING, RunStatus.CANCELLED},
    RunStatus.INPUT_VALIDATING: {RunStatus.CLASSIFYING, RunStatus.FAILED},
    RunStatus.CLASSIFYING: {RunStatus.EXTRACTING, RunStatus.FAILED},
    RunStatus.EXTRACTING: {RunStatus.IR_VALIDATING, RunStatus.FAILED},
    RunStatus.IR_VALIDATING: {RunStatus.WAITING_FOR_USER_REVIEW, RunStatus.REPAIRING, RunStatus.FAILED},
    RunStatus.WAITING_FOR_USER_REVIEW: {RunStatus.GENERATING, RunStatus.CANCELLED, RunStatus.REJECTED},
    RunStatus.GENERATING: {RunStatus.VALIDATING_OUTPUT, RunStatus.FAILED},
    RunStatus.VALIDATING_OUTPUT: {RunStatus.PUBLISHING, RunStatus.REPAIRING, RunStatus.WAITING_FOR_APPROVAL, RunStatus.FAILED},
    RunStatus.REPAIRING: {RunStatus.EXTRACTING, RunStatus.GENERATING, RunStatus.WAITING_FOR_APPROVAL, RunStatus.FAILED},
    RunStatus.WAITING_FOR_APPROVAL: {RunStatus.GENERATING, RunStatus.PUBLISHING, RunStatus.REJECTED},
    RunStatus.PUBLISHING: {RunStatus.COMPLETED, RunStatus.FAILED},
}

def ensure_transition(current: RunStatus, target: RunStatus) -> None:
    if target not in _ALLOWED.get(current, set()):
        raise ValueError(f"Illegal run transition: {current} -> {target}")
