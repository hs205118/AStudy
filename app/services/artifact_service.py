"""教学注释版：app/services/artifact_service.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import json, uuid
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy import select
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from sqlalchemy.orm import Session
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import ArtifactKind
# [教学注释 L5] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.artifact_store import ArtifactStore
# [教学注释 L6] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.infrastructure.database import ArtifactRecord

# [教学注释 L8] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ArtifactService:
    # [教学注释 L9] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self, db: Session, store: ArtifactStore):
        # [教学注释 L10] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self.db, self.store = db, store

    # [教学注释 L12] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def create_json(self, run_id: str, kind: ArtifactKind, name: str, payload: dict, revision: int = 1) -> ArtifactRecord:
        # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        artifact_id = str(uuid.uuid4())
        # [教学注释 L14] 把 Python 对象序列化为 JSON，作为稳定的文件或网络交换格式。
        content = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        uri, digest = self.store.put(f"{run_id}/{artifact_id}/{name}", content)
        # [教学注释 L16] 计算内容哈希，用于完整性校验、审计和后续去重。
        row = ArtifactRecord(id=artifact_id, run_id=run_id, kind=kind.value, name=name, media_type="application/json", uri=uri, sha256=digest, revision=revision)
        # [教学注释 L17] 提交当前数据库事务，使此前修改成为持久状态。
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        # [教学注释 L18] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return row

    # [教学注释 L20] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def list_for_run(self, run_id: str) -> list[ArtifactRecord]:
        # [教学注释 L21] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return list(self.db.scalars(select(ArtifactRecord).where(ArtifactRecord.run_id == run_id).order_by(ArtifactRecord.created_at)))

    # [教学注释 L23] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def read_json(self, artifact: ArtifactRecord) -> dict:
        # [教学注释 L24] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return json.loads(self.store.get(artifact.uri))
