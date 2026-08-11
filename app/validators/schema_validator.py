from typing import Any
from jsonschema import Draft202012Validator
from app.domain.enums import Severity
from app.domain.schemas import Finding

class JsonSchemaValidator:
    id = "json-schema"
    version = "1.0.0"
    def __init__(self, schema: dict[str, Any]):
        self.schema = schema
    def validate(self, payload: dict[str, Any], context: dict[str, Any]) -> list[Finding]:
        findings = []
        for error in sorted(Draft202012Validator(self.schema).iter_errors(payload), key=lambda e: list(e.path)):
            findings.append(Finding(rule_id="schema", severity=Severity.ERROR, message=error.message, location="/" + "/".join(map(str, error.path))))
        return findings
