from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from app.domain.enums import ArtifactKind, RunStatus, Severity

class RunCreate(BaseModel):
    module_id: str
    module_version: str = "1.0.0"
    parameters: dict[str, Any] = Field(default_factory=dict)
    input_text: str | None = None
    input_artifact_ids: list[str] = Field(default_factory=list)

class RunRead(BaseModel):
    id: str
    module_id: str
    module_version: str
    status: RunStatus
    parameters: dict[str, Any]
    current_step: str | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

class ArtifactRead(BaseModel):
    id: str
    run_id: str
    kind: ArtifactKind
    name: str
    media_type: str
    uri: str
    sha256: str
    revision: int
    created_at: datetime

class Finding(BaseModel):
    rule_id: str
    severity: Severity
    message: str
    location: str | None = None
    expected: Any = None
    actual: Any = None
    repair_hint: str | None = None

class ValidationReport(BaseModel):
    valid: bool
    findings: list[Finding] = Field(default_factory=list)
    validator_versions: dict[str, str] = Field(default_factory=dict)

class UserPatchRequest(BaseModel):
    patch: list[dict[str, Any]]
    comment: str | None = None

class ApprovalRequest(BaseModel):
    approved: bool
    comment: str | None = None
