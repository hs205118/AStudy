"""教学注释版：app/services/run_service.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import uuid
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy import select
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy.orm import Session
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import RunStatus
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import RunCreate
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import RunRecord, utcnow
# [教学注释 L7] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.core.state_machine import ensure_transition

# [教学注释 L9] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class RunService:
    # [教学注释 L10] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self, db: Session): self.db = db
    # [教学注释 L11] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def create(self, request: RunCreate) -> RunRecord:
        # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        row = RunRecord(id=str(uuid.uuid4()), module_id=request.module_id, module_version=request.module_version, status=RunStatus.CREATED.value, parameters=request.parameters, input_text=request.input_text)
        # [教学注释 L13] 提交当前数据库事务，使此前修改成为持久状态。
        self.db.add(row); self.db.commit(); self.db.refresh(row); return row
    # [教学注释 L14] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def get(self, run_id: str) -> RunRecord:
        # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        row = self.db.scalar(select(RunRecord).where(RunRecord.id == run_id))
        # [教学注释 L16] 根据当前状态或输入条件选择执行分支。
        if not row: raise KeyError(run_id)
        # [教学注释 L17] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return row
    # [教学注释 L18] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def transition(self, row: RunRecord, target: RunStatus, step: str | None = None) -> None:
        # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        ensure_transition(RunStatus(row.status), target)
        # [教学注释 L20] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        row.status = target.value; row.current_step = step; row.updated_at = utcnow()
        # [教学注释 L21] 提交当前数据库事务，使此前修改成为持久状态。
        self.db.commit(); self.db.refresh(row)
    # [教学注释 L22] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def fail(self, row: RunRecord, error: str) -> None:
        # [教学注释 L23] 提交当前数据库事务，使此前修改成为持久状态。
        row.status = RunStatus.FAILED.value; row.error = error; row.updated_at = utcnow(); self.db.commit()
