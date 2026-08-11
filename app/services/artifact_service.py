import json, uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.enums import ArtifactKind
from app.infrastructure.artifact_store import ArtifactStore
from app.infrastructure.database import ArtifactRecord

class ArtifactService:
    def __init__(self, db: Session, store: ArtifactStore):
        self.db, self.store = db, store

    def create_json(self, run_id: str, kind: ArtifactKind, name: str, payload: dict, revision: int = 1) -> ArtifactRecord:
        artifact_id = str(uuid.uuid4())
        content = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        uri, digest = self.store.put(f"{run_id}/{artifact_id}/{name}", content)
        row = ArtifactRecord(id=artifact_id, run_id=run_id, kind=kind.value, name=name, media_type="application/json", uri=uri, sha256=digest, revision=revision)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return row

    def list_for_run(self, run_id: str) -> list[ArtifactRecord]:
        return list(self.db.scalars(select(ArtifactRecord).where(ArtifactRecord.run_id == run_id).order_by(ArtifactRecord.created_at)))

    def read_json(self, artifact: ArtifactRecord) -> dict:
        return json.loads(self.store.get(artifact.uri))
