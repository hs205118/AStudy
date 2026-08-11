from typing import Any
from app.domain.enums import Severity
from app.domain.schemas import Finding

class StorageBusinessValidator:
    id = "storage-business-rules"
    version = "1.0.0"
    def validate(self, payload: dict[str, Any], context: dict[str, Any]) -> list[Finding]:
        findings = []
        entities = payload.get("entities", {})
        count = entities.get("drive_count")
        if count is not None and count < 1:
            findings.append(Finding(rule_id="storage.drive_count.positive", severity=Severity.ERROR, message="drive_count must be positive", location="/entities/drive_count", actual=count, expected=">= 1"))
        if not payload.get("requirements"):
            findings.append(Finding(rule_id="storage.requirements.required", severity=Severity.BLOCKER, message="At least one requirement is required", location="/requirements"))
        return findings
