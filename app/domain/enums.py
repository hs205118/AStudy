from enum import StrEnum

class RunStatus(StrEnum):
    CREATED = "CREATED"
    INPUT_VALIDATING = "INPUT_VALIDATING"
    CLASSIFYING = "CLASSIFYING"
    EXTRACTING = "EXTRACTING"
    IR_VALIDATING = "IR_VALIDATING"
    WAITING_FOR_USER_REVIEW = "WAITING_FOR_USER_REVIEW"
    GENERATING = "GENERATING"
    VALIDATING_OUTPUT = "VALIDATING_OUTPUT"
    REPAIRING = "REPAIRING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    PUBLISHING = "PUBLISHING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class ArtifactKind(StrEnum):
    INPUT = "input"
    INTERMEDIATE = "intermediate"
    CANDIDATE = "candidate"
    VALIDATION_REPORT = "validation_report"
    FINAL = "final"

class Severity(StrEnum):
    BLOCKER = "blocker"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
