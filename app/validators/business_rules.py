"""教学注释版：app/validators/business_rules.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import Severity
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import Finding

# [教学注释 L5] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class StorageBusinessValidator:
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id = "storage-business-rules"
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version = "1.0.0"
    # [教学注释 L8] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def validate(self, payload: dict[str, Any], context: dict[str, Any]) -> list[Finding]:
        # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        findings = []
        # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        entities = payload.get("entities", {})
        # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        count = entities.get("drive_count")
        # [教学注释 L12] 根据当前状态或输入条件选择执行分支。
        if count is not None and count < 1:
            # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            findings.append(Finding(rule_id="storage.drive_count.positive", severity=Severity.ERROR, message="drive_count must be positive", location="/entities/drive_count", actual=count, expected=">= 1"))
        # [教学注释 L14] 根据当前状态或输入条件选择执行分支。
        if not payload.get("requirements"):
            # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
            findings.append(Finding(rule_id="storage.requirements.required", severity=Severity.BLOCKER, message="At least one requirement is required", location="/requirements"))
        # [教学注释 L16] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return findings
