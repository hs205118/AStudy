import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.enums import RunStatus
from app.domain.schemas import RunCreate
from app.infrastructure.database import RunRecord, utcnow
from app.core.state_machine import ensure_transition

class RunService:
    def __init__(self, db: Session): self.db = db
    def create(self, request: RunCreate) -> RunRecord:
        row = RunRecord(id=str(uuid.uuid4()), module_id=request.module_id, module_version=request.module_version, status=RunStatus.CREATED.value, parameters=request.parameters, input_text=request.input_text)
        self.db.add(row); self.db.commit(); self.db.refresh(row); return row
    def get(self, run_id: str) -> RunRecord:
        row = self.db.scalar(select(RunRecord).where(RunRecord.id == run_id))
        if not row: raise KeyError(run_id)
        return row
    def transition(self, row: RunRecord, target: RunStatus, step: str | None = None) -> None:
        ensure_transition(RunStatus(row.status), target)
        row.status = target.value; row.current_step = step; row.updated_at = utcnow()
        self.db.commit(); self.db.refresh(row)
    def fail(self, row: RunRecord, error: str) -> None:
        row.status = RunStatus.FAILED.value; row.error = error; row.updated_at = utcnow(); self.db.commit()
