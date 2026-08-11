import json
from jsonschema import Draft202012Validator
from sqlalchemy.orm import Session
from app.domain.enums import ArtifactKind, RunStatus, Severity
from app.domain.schemas import Finding, ValidationReport
from app.services.artifact_service import ArtifactService
from app.services.module_registry import ModuleRegistry
from app.services.model_provider import ModelProvider
from app.services.run_service import RunService
from app.validators.business_rules import StorageBusinessValidator
from app.validators.schema_validator import JsonSchemaValidator

class Orchestrator:
    def __init__(self, db: Session, modules: ModuleRegistry, artifacts: ArtifactService, model: ModelProvider, max_repairs: int = 2):
        self.db, self.modules, self.artifacts, self.model, self.max_repairs = db, modules, artifacts, model, max_repairs
        self.runs = RunService(db)

    def execute_until_review(self, run_id: str):
        run = self.runs.get(run_id)
        try:
            module = self.modules.get(run.module_id, run.module_version)
            self.runs.transition(run, RunStatus.INPUT_VALIDATING, "validate_input")
            if not run.input_text and not run.parameters:
                raise ValueError("At least input_text or parameters must be provided")
            self.runs.transition(run, RunStatus.CLASSIFYING, "resolve_module")
            self.runs.transition(run, RunStatus.EXTRACTING, "extract_ir")
            system_prompt = self.modules.read_relative(module, module.raw["prompts"]["system"])
            schema = json.loads(self.modules.read_relative(module, module.raw["schemas"]["ir"]))
            ir = self.model.structured_extract(system_prompt=system_prompt, user_content=run.input_text or json.dumps(run.parameters), schema=schema)
            self.artifacts.create_json(run.id, ArtifactKind.INTERMEDIATE, "ir.json", ir)
            self.runs.transition(run, RunStatus.IR_VALIDATING, "validate_ir")
            errors = list(Draft202012Validator(schema).iter_errors(ir))
            if errors:
                raise ValueError("IR schema validation failed: " + "; ".join(e.message for e in errors))
            self.runs.transition(run, RunStatus.WAITING_FOR_USER_REVIEW, "review_ir")
            return run
        except Exception as exc:
            self.runs.fail(run, str(exc)); raise

    def generate_and_validate(self, run_id: str):
        run = self.runs.get(run_id)
        if RunStatus(run.status) not in {RunStatus.WAITING_FOR_USER_REVIEW, RunStatus.WAITING_FOR_APPROVAL}:
            raise ValueError("Run is not ready for generation")
        module = self.modules.get(run.module_id, run.module_version)
        self.runs.transition(run, RunStatus.GENERATING, "generate_candidate")
        ir_artifacts = [a for a in self.artifacts.list_for_run(run.id) if a.kind == ArtifactKind.INTERMEDIATE.value]
        if not ir_artifacts: raise ValueError("No IR artifact")
        ir = self.artifacts.read_json(ir_artifacts[-1])
        candidate = {"format_version": "1.0", "product": run.parameters.get("product", "unknown"), "requirements": ir.get("requirements", []), "entities": ir.get("entities", {})}
        self.artifacts.create_json(run.id, ArtifactKind.CANDIDATE, "candidate.json", candidate)
        self.runs.transition(run, RunStatus.VALIDATING_OUTPUT, "validate_candidate")
        output_schema = json.loads(self.modules.read_relative(module, module.raw["schemas"]["output"]))
        findings: list[Finding] = []
        findings.extend(JsonSchemaValidator(output_schema).validate(candidate, {}))
        findings.extend(StorageBusinessValidator().validate(candidate, {}))
        for f in self.model.semantic_validate(source=run.input_text or "", candidate=candidate):
            findings.append(Finding(**f))
        valid = not any(f.severity in {Severity.BLOCKER, Severity.ERROR} for f in findings)
        report = ValidationReport(valid=valid, findings=findings, validator_versions={"json-schema": "1.0.0", "storage-business-rules": "1.0.0"})
        self.artifacts.create_json(run.id, ArtifactKind.VALIDATION_REPORT, "validation-report.json", report.model_dump(mode="json"))
        if not valid:
            self.runs.transition(run, RunStatus.WAITING_FOR_APPROVAL, "manual_resolution")
            return run
        self.runs.transition(run, RunStatus.PUBLISHING, "publish")
        self.artifacts.create_json(run.id, ArtifactKind.FINAL, "final.json", candidate)
        self.runs.transition(run, RunStatus.COMPLETED, "completed")
        return run
