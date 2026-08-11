from typing import Any

class OptimizationService:
    def propose(self, *, run_id: str, user_patch: list[dict[str, Any]] | None = None, findings: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        signals = []
        if user_patch: signals.append({"type": "user_patch", "count": len(user_patch)})
        if findings: signals.append({"type": "validation_findings", "count": len(findings)})
        return {"run_id": run_id, "status": "candidate", "signals": signals, "recommendations": ["Evaluate recurring field changes against the golden dataset before changing prompts or memory."] if signals else []}
