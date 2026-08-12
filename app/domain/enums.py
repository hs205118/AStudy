"""教学注释版：app/domain/enums.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from enum import StrEnum

# [教学注释 L3] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class RunStatus(StrEnum):
    # [教学注释 L4] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    CREATED = "CREATED"
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    INPUT_VALIDATING = "INPUT_VALIDATING"
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    CLASSIFYING = "CLASSIFYING"
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    EXTRACTING = "EXTRACTING"
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    IR_VALIDATING = "IR_VALIDATING"
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    WAITING_FOR_USER_REVIEW = "WAITING_FOR_USER_REVIEW"
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    GENERATING = "GENERATING"
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    VALIDATING_OUTPUT = "VALIDATING_OUTPUT"
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    REPAIRING = "REPAIRING"
    # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    PUBLISHING = "PUBLISHING"
    # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    COMPLETED = "COMPLETED"
    # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    FAILED = "FAILED"
    # [教学注释 L17] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    CANCELLED = "CANCELLED"
    # [教学注释 L18] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    REJECTED = "REJECTED"

# [教学注释 L20] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ArtifactKind(StrEnum):
    # [教学注释 L21] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    INPUT = "input"
    # [教学注释 L22] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    INTERMEDIATE = "intermediate"
    # [教学注释 L23] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    CANDIDATE = "candidate"
    # [教学注释 L24] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    VALIDATION_REPORT = "validation_report"
    # [教学注释 L25] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    FINAL = "final"

# [教学注释 L27] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Severity(StrEnum):
    # [教学注释 L28] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    BLOCKER = "blocker"
    # [教学注释 L29] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    ERROR = "error"
    # [教学注释 L30] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    WARNING = "warning"
    # [教学注释 L31] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    INFO = "info"
