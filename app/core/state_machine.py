"""教学注释版：app/core/state_machine.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import RunStatus

# [教学注释 L3] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
_ALLOWED = {
    # [教学注释 L4] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.CREATED: {RunStatus.INPUT_VALIDATING, RunStatus.CANCELLED},
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.INPUT_VALIDATING: {RunStatus.CLASSIFYING, RunStatus.FAILED},
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.CLASSIFYING: {RunStatus.EXTRACTING, RunStatus.FAILED},
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.EXTRACTING: {RunStatus.IR_VALIDATING, RunStatus.FAILED},
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.IR_VALIDATING: {RunStatus.WAITING_FOR_USER_REVIEW, RunStatus.REPAIRING, RunStatus.FAILED},
    # [教学注释 L9] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.WAITING_FOR_USER_REVIEW: {RunStatus.GENERATING, RunStatus.CANCELLED, RunStatus.REJECTED},
    # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.GENERATING: {RunStatus.VALIDATING_OUTPUT, RunStatus.FAILED},
    # [教学注释 L11] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.VALIDATING_OUTPUT: {RunStatus.PUBLISHING, RunStatus.REPAIRING, RunStatus.WAITING_FOR_APPROVAL, RunStatus.FAILED},
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.REPAIRING: {RunStatus.EXTRACTING, RunStatus.GENERATING, RunStatus.WAITING_FOR_APPROVAL, RunStatus.FAILED},
    # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.WAITING_FOR_APPROVAL: {RunStatus.GENERATING, RunStatus.PUBLISHING, RunStatus.REJECTED},
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    RunStatus.PUBLISHING: {RunStatus.COMPLETED, RunStatus.FAILED},
# [教学注释 L15] 结束上一行开始的复合表达式或参数列表。
}

# [教学注释 L17] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def ensure_transition(current: RunStatus, target: RunStatus) -> None:
    # [教学注释 L18] 根据当前状态或输入条件选择执行分支。
    if target not in _ALLOWED.get(current, set()):
        # [教学注释 L19] 主动终止当前路径并向上层报告受控错误，避免静默产生错误结果。
        raise ValueError(f"Illegal run transition: {current} -> {target}")
