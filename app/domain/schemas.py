"""教学注释版：app/domain/schemas.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from datetime import datetime
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from pydantic import BaseModel, Field
# [教学注释 L4] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import ArtifactKind, RunStatus, Severity

# [教学注释 L6] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class RunCreate(BaseModel):
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_id: str
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_version: str = "1.0.0"
    # [教学注释 L9] 为 Pydantic 字段指定安全默认值或额外校验信息。
    parameters: dict[str, Any] = Field(default_factory=dict)
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    input_text: str | None = None
    # [教学注释 L11] 为 Pydantic 字段指定安全默认值或额外校验信息。
    input_artifact_ids: list[str] = Field(default_factory=list)

# [教学注释 L13] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class RunRead(BaseModel):
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id: str
    # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_id: str
    # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_version: str
    # [教学注释 L17] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    status: RunStatus
    # [教学注释 L18] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    parameters: dict[str, Any]
    # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    current_step: str | None = None
    # [教学注释 L20] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    error: str | None = None
    # [教学注释 L21] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    created_at: datetime
    # [教学注释 L22] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    updated_at: datetime

# [教学注释 L24] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ArtifactRead(BaseModel):
    # [教学注释 L25] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id: str
    # [教学注释 L26] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    run_id: str
    # [教学注释 L27] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    kind: ArtifactKind
    # [教学注释 L28] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    name: str
    # [教学注释 L29] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    media_type: str
    # [教学注释 L30] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    uri: str
    # [教学注释 L31] 计算内容哈希，用于完整性校验、审计和后续去重。
    sha256: str
    # [教学注释 L32] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    revision: int
    # [教学注释 L33] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    created_at: datetime

# [教学注释 L35] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Finding(BaseModel):
    # [教学注释 L36] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    rule_id: str
    # [教学注释 L37] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    severity: Severity
    # [教学注释 L38] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    message: str
    # [教学注释 L39] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    location: str | None = None
    # [教学注释 L40] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    expected: Any = None
    # [教学注释 L41] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    actual: Any = None
    # [教学注释 L42] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    repair_hint: str | None = None

# [教学注释 L44] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ValidationReport(BaseModel):
    # [教学注释 L45] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    valid: bool
    # [教学注释 L46] 为 Pydantic 字段指定安全默认值或额外校验信息。
    findings: list[Finding] = Field(default_factory=list)
    # [教学注释 L47] 为 Pydantic 字段指定安全默认值或额外校验信息。
    validator_versions: dict[str, str] = Field(default_factory=dict)

# [教学注释 L49] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class UserPatchRequest(BaseModel):
    # [教学注释 L50] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    patch: list[dict[str, Any]]
    # [教学注释 L51] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    comment: str | None = None

# [教学注释 L53] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ApprovalRequest(BaseModel):
    # [教学注释 L54] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    approved: bool
    # [教学注释 L55] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    comment: str | None = None
