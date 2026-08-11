from app.container import artifact_store, model_provider, module_registry
from app.domain.schemas import RunCreate
from app.infrastructure.database import SessionLocal, init_db
from app.services.artifact_service import ArtifactService
from app.services.orchestrator import Orchestrator
from app.services.run_service import RunService

if __name__ == "__main__":
    init_db()
    with SessionLocal() as db:
        run = RunService(db).create(RunCreate(module_id="storage-wizard", parameters={"product": "demo-server"}, input_text="Storage controller requires RAID 1 and 4 NVMe drives."))
        orch = Orchestrator(db, module_registry(), ArtifactService(db, artifact_store()), model_provider())
        orch.execute_until_review(run.id)
        orch.generate_and_validate(run.id)
        final = RunService(db).get(run.id)
        print({"run_id": final.id, "status": final.status, "artifacts": [a.name for a in ArtifactService(db, artifact_store()).list_for_run(final.id)]})
