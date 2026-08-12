"""教学注释版：app/api/routes/runs.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from fastapi import APIRouter, Depends, HTTPException
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy.orm import Session
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.api.dependencies import require_api_key
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.config import get_settings
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.container import artifact_store, model_provider, module_registry
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import ArtifactKind
# [教学注释 L7] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import ArtifactRead, RunCreate, RunRead, UserPatchRequest
# [教学注释 L8] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import get_db
# [教学注释 L9] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.artifact_service import ArtifactService
# [教学注释 L10] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.orchestrator import Orchestrator
# [教学注释 L11] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.patch_service import apply_json_patch
# [教学注释 L12] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.run_service import RunService

# [教学注释 L14] 要求 FastAPI 通过依赖注入提供资源，常用于数据库会话或鉴权。
router = APIRouter(prefix="/runs", tags=["runs"], dependencies=[Depends(require_api_key)])

# [教学注释 L16] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def to_run(row):
    # [教学注释 L17] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return RunRead(id=row.id, module_id=row.module_id, module_version=row.module_version, status=row.status, parameters=row.parameters, current_step=row.current_step, error=row.error, created_at=row.created_at, updated_at=row.updated_at)

# [教学注释 L19] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.post("", response_model=RunRead, status_code=201)
# [教学注释 L20] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def create_run(request: RunCreate, db: Session = Depends(get_db)):
    # [教学注释 L21] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try: module_registry().get(request.module_id, request.module_version)
    # [教学注释 L22] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    # [教学注释 L23] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return to_run(RunService(db).create(request))

# [教学注释 L25] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.get("/{run_id}", response_model=RunRead)
# [教学注释 L26] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def get_run(run_id: str, db: Session = Depends(get_db)):
    # [教学注释 L27] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try: return to_run(RunService(db).get(run_id))
    # [教学注释 L28] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except KeyError as exc: raise HTTPException(404, "Run not found") from exc

# [教学注释 L30] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.post("/{run_id}/execute", response_model=RunRead)
# [教学注释 L31] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def execute(run_id: str, db: Session = Depends(get_db)):
    # [教学注释 L32] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    service = ArtifactService(db, artifact_store())
    # [教学注释 L33] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    orch = Orchestrator(db, module_registry(), service, model_provider(), get_settings().max_repair_attempts)
    # [教学注释 L34] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try: return to_run(orch.execute_until_review(run_id))
    # [教学注释 L35] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    # [教学注释 L36] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc

# [教学注释 L38] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.post("/{run_id}/generate", response_model=RunRead)
# [教学注释 L39] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def generate(run_id: str, db: Session = Depends(get_db)):
    # [教学注释 L40] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    service = ArtifactService(db, artifact_store())
    # [教学注释 L41] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    orch = Orchestrator(db, module_registry(), service, model_provider(), get_settings().max_repair_attempts)
    # [教学注释 L42] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try: return to_run(orch.generate_and_validate(run_id))
    # [教学注释 L43] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except KeyError as exc: raise HTTPException(404, str(exc)) from exc
    # [教学注释 L44] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc

# [教学注释 L46] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.get("/{run_id}/artifacts", response_model=list[ArtifactRead])
# [教学注释 L47] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def list_artifacts(run_id: str, db: Session = Depends(get_db)):
    # [教学注释 L48] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    rows = ArtifactService(db, artifact_store()).list_for_run(run_id)
    # [教学注释 L49] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return [ArtifactRead(id=a.id, run_id=a.run_id, kind=a.kind, name=a.name, media_type=a.media_type, uri=a.uri, sha256=a.sha256, revision=a.revision, created_at=a.created_at) for a in rows]

# [教学注释 L51] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@router.post("/{run_id}/ir/patch", response_model=ArtifactRead)
# [教学注释 L52] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def patch_ir(run_id: str, request: UserPatchRequest, db: Session = Depends(get_db)):
    # [教学注释 L53] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    artifacts = ArtifactService(db, artifact_store())
    # [教学注释 L54] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    irs = [a for a in artifacts.list_for_run(run_id) if a.kind == ArtifactKind.INTERMEDIATE.value]
    # [教学注释 L55] 根据当前状态或输入条件选择执行分支。
    if not irs: raise HTTPException(404, "IR not found")
    # [教学注释 L56] 开始可能失败的操作，并在后续分支中把异常转换为可诊断结果。
    try: updated = apply_json_patch(artifacts.read_json(irs[-1]), request.patch)
    # [教学注释 L57] 捕获指定异常，防止底层错误直接泄漏为不可理解的故障。
    except (KeyError, IndexError, ValueError, TypeError) as exc: raise HTTPException(422, str(exc)) from exc
    # [教学注释 L58] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    row = artifacts.create_json(run_id, ArtifactKind.INTERMEDIATE, f"ir-r{irs[-1].revision + 1}.json", updated, irs[-1].revision + 1)
    # [教学注释 L59] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
    return ArtifactRead(id=row.id, run_id=row.run_id, kind=row.kind, name=row.name, media_type=row.media_type, uri=row.uri, sha256=row.sha256, revision=row.revision, created_at=row.created_at)
