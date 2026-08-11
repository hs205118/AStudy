from typing import Any, Protocol
from app.domain.schemas import Finding

class Validator(Protocol):
    id: str
    version: str
    def validate(self, payload: dict[str, Any], context: dict[str, Any]) -> list[Finding]: ...
