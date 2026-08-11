from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import require_api_key
from app.config import get_settings
from app.container import artifact_store, model_provider, module_registry
from app.domain.enums import ArtifactKind
from app.domain.schemas import ArtifactRead, RunCreate, RunRead, UserPatchRequest
from app.infrastructure.database import get_db
from app.services.artifact_service import ArtifactService
from app.services.orchestrator import Orchestrator
from app.services.patch_service import apply_json_patch
from app.services.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"], dependencies=[Depends(require_api_key)])

def to_run(row):
    return RunRead(id=row.id, module_id=row.module_id, module_version=row.module_version, status=row.status, parameters=row.parameters, current_step=row.current_step, error=row.error, created_at=row.created_at, updated_at=row.updated_at)

@router.post("", response_model=RunRead, status_code=201)
def create_run(request: RunCreate, db: Session = Depends(get_db)):
    try: module_registry().get(request.module_id, request.module_version)
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    return to_run(RunService(db).create(request))

@router.get("/{run_id}", response_model=RunRead)
def get_run(run_id: str, db: Session = Depends(get_db)):
    try: return to_run(RunService(db).get(run_id))
    except KeyError as exc: raise HTTPException(404, "Run not found") from exc

@router.post("/{run_id}/execute", response_model=RunRead)
def execute(run_id: str, db: Session = Depends(get_db)):
    service = ArtifactService(db, artifact_store())
    orch = Orchestrator(db, module_registry(), service, model_provider(), get_settings().max_repair_attempts)
    try: return to_run(orch.execute_until_review(run_id))
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc

@router.post("/{run_id}/generate", response_model=RunRead)
def generate(run_id: str, db: Session = Depends(get_db)):
    service = ArtifactService(db, artifact_store())
    orch = Orchestrator(db, module_registry(), service, model_provider(), get_settings().max_repair_attempts)
    try: return to_run(orch.generate_and_validate(run_id))
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc

@router.get("/{run_id}/artifacts", response_model=list[ArtifactRead])
def list_artifacts(run_id: str, db: Session = Depends(get_db)):
    rows = ArtifactService(db, artifact_store()).list_for_run(run_id)
    return [ArtifactRead(id=a.id, run_id=a.run_id, kind=a.kind, name=a.name, media_type=a.media_type, uri=a.uri, sha256=a.sha256, revision=a.revision, created_at=a.created_at) for a in rows]

@router.post("/{run_id}/ir/patch", response_model=ArtifactRead)
def patch_ir(run_id: str, request: UserPatchRequest, db: Session = Depends(get_db)):
    artifacts = ArtifactService(db, artifact_store())
    irs = [a for a in artifacts.list_for_run(run_id) if a.kind == ArtifactKind.INTERMEDIATE.value]
    if not irs: raise HTTPException(404, "IR not found")
    try: updated = apply_json_patch(artifacts.read_json(irs[-1]), request.patch)
    except (KeyError, IndexError, ValueError, TypeError) as exc: raise HTTPException(422, str(exc)) from exc
    row = artifacts.create_json(run_id, ArtifactKind.INTERMEDIATE, f"ir-r{irs[-1].revision + 1}.json", updated, irs[-1].revision + 1)
    return ArtifactRead(id=row.id, run_id=row.run_id, kind=row.kind, name=row.name, media_type=row.media_type, uri=row.uri, sha256=row.sha256, revision=row.revision, created_at=row.created_at)
