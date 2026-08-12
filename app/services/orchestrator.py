"""教学注释版：app/services/orchestrator.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import json
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from jsonschema import Draft202012Validator
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy.orm import Session
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import ArtifactKind, RunStatus, Severity
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import Finding, ValidationReport
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.artifact_service import ArtifactService
# [教学注释 L7] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.module_registry import ModuleRegistry
# [教学注释 L8] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.model_provider import ModelProvider
# [教学注释 L9] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.run_service import RunService
# [教学注释 L10] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.validators.business_rules import StorageBusinessValidator
# [教学注释 L11] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.validators.schema_validator import JsonSchemaValidator

# [教学注释 L13] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Orchestrator:
    # [教学注释 L14] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self, db: Session, modules: ModuleRegistry, artifacts: ArtifactService, model: ModelProvider, max_repairs: int = 2):
        # [教学注释 L15] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.db, self.modules, self.artifacts, self.model, self.max_repairs = db, modules, artifacts, model, max_repairs
        # [教学注释 L16] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.runs = RunService(db)

    # [教学注释 L18] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def execute_until_review(self, run_id: str):
        # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        run = self.runs.get(run_id)
        # [教学注释 L20] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
        try:
            # [教学注释 L21] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            module = self.modules.get(run.module_id, run.module_version)
            # [教学注释 L22] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.INPUT_VALIDATING, "validate_input")
            # [教学注释 L23] 根据当前状态或输入条件选择执行分支。
            if not run.input_text and not run.parameters:
                # [教学注释 L24] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
                raise ValueError("At least input_text or parameters must be provided")
            # [教学注释 L25] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.CLASSIFYING, "resolve_module")
            # [教学注释 L26] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.EXTRACTING, "extract_ir")
            # [教学注释 L27] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            system_prompt = self.modules.read_relative(module, module.raw["prompts"]["system"])
            # [教学注释 L28] 把 JSON 文本解析为 Python 对象；上层仍需进行 Schema 校验。
            schema = json.loads(self.modules.read_relative(module, module.raw["schemas"]["ir"]))
            # [教学注释 L29] 把 Python 对象序列化为 JSON，作为稳定的文件或网络交换格式。
            ir = self.model.structured_extract(system_prompt=system_prompt, user_content=run.input_text or json.dumps(run.parameters), schema=schema)
            # [教学注释 L30] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.artifacts.create_json(run.id, ArtifactKind.INTERMEDIATE, "ir.json", ir)
            # [教学注释 L31] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.IR_VALIDATING, "validate_ir")
            # [教学注释 L32] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            errors = list(Draft202012Validator(schema).iter_errors(ir))
            # [教学注释 L33] 根据当前状态或输入条件选择执行分支。
            if errors:
                # [教学注释 L34] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
                raise ValueError("IR schema validation failed: " + "; ".join(e.message for e in errors))
            # [教学注释 L35] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.WAITING_FOR_USER_REVIEW, "review_ir")
            # [教学注释 L36] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
            return run
        # [教学注释 L37] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
        except Exception as exc:
            # [教学注释 L38] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.fail(run, str(exc)); raise

    # [教学注释 L40] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def generate_and_validate(self, run_id: str):
        # [教学注释 L41] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        run = self.runs.get(run_id)
        # [教学注释 L42] 根据当前状态或输入条件选择执行分支。
        if RunStatus(run.status) not in {RunStatus.WAITING_FOR_USER_REVIEW, RunStatus.WAITING_FOR_APPROVAL}:
            # [教学注释 L43] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
            raise ValueError("Run is not ready for generation")
        # [教学注释 L44] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        module = self.modules.get(run.module_id, run.module_version)
        # [教学注释 L45] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.runs.transition(run, RunStatus.GENERATING, "generate_candidate")
        # [教学注释 L46] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        ir_artifacts = [a for a in self.artifacts.list_for_run(run.id) if a.kind == ArtifactKind.INTERMEDIATE.value]
        # [教学注释 L47] 根据当前状态或输入条件选择执行分支。
        if not ir_artifacts: raise ValueError("No IR artifact")
        # [教学注释 L48] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        ir = self.artifacts.read_json(ir_artifacts[-1])
        # [教学注释 L49] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        candidate = {"format_version": "1.0", "product": run.parameters.get("product", "unknown"), "requirements": ir.get("requirements", []), "entities": ir.get("entities", {})}
        # [教学注释 L50] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.artifacts.create_json(run.id, ArtifactKind.CANDIDATE, "candidate.json", candidate)
        # [教学注释 L51] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.runs.transition(run, RunStatus.VALIDATING_OUTPUT, "validate_candidate")
        # [教学注释 L52] 把 JSON 文本解析为 Python 对象；上层仍需进行 Schema 校验。
        output_schema = json.loads(self.modules.read_relative(module, module.raw["schemas"]["output"]))
        # [教学注释 L53] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        findings: list[Finding] = []
        # [教学注释 L54] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        findings.extend(JsonSchemaValidator(output_schema).validate(candidate, {}))
        # [教学注释 L55] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        findings.extend(StorageBusinessValidator().validate(candidate, {}))
        # [教学注释 L56] 遍历集合中的每个元素，逐项执行相同规则。
        for f in self.model.semantic_validate(source=run.input_text or "", candidate=candidate):
            # [教学注释 L57] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            findings.append(Finding(**f))
        # [教学注释 L58] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        valid = not any(f.severity in {Severity.BLOCKER, Severity.ERROR} for f in findings)
        # [教学注释 L59] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        report = ValidationReport(valid=valid, findings=findings, validator_versions={"json-schema": "1.0.0", "storage-business-rules": "1.0.0"})
        # [教学注释 L60] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.artifacts.create_json(run.id, ArtifactKind.VALIDATION_REPORT, "validation-report.json", report.model_dump(mode="json"))
        # [教学注释 L61] 根据当前状态或输入条件选择执行分支。
        if not valid:
            # [教学注释 L62] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            self.runs.transition(run, RunStatus.WAITING_FOR_APPROVAL, "manual_resolution")
            # [教学注释 L63] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
            return run
        # [教学注释 L64] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.runs.transition(run, RunStatus.PUBLISHING, "publish")
        # [教学注释 L65] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.artifacts.create_json(run.id, ArtifactKind.FINAL, "final.json", candidate)
        # [教学注释 L66] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        self.runs.transition(run, RunStatus.COMPLETED, "completed")
        # [教学注释 L67] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return run
