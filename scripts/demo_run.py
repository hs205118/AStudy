"""教学注释版：scripts/demo_run.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.container import artifact_store, model_provider, module_registry
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import RunCreate
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import SessionLocal, init_db
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.artifact_service import ArtifactService
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.orchestrator import Orchestrator
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.services.run_service import RunService

# [教学注释 L8] 根据当前状态或输入条件选择执行分支。
if __name__ == "__main__":
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    init_db()
    # [教学注释 L10] 通过上下文管理器确保资源在离开代码块时被正确释放。
    with SessionLocal() as db:
        # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        run = RunService(db).create(RunCreate(module_id="storage-wizard", parameters={"product": "demo-server"}, input_text="Storage controller requires RAID 1 and 4 NVMe drives."))
        # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        orch = Orchestrator(db, module_registry(), ArtifactService(db, artifact_store()), model_provider())
        # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        orch.execute_until_review(run.id)
        # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        orch.generate_and_validate(run.id)
        # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        final = RunService(db).get(run.id)
        # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        print({"run_id": final.id, "status": final.status, "artifacts": [a.name for a in ArtifactService(db, artifact_store()).list_for_run(final.id)]})
