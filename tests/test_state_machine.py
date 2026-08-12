"""教学注释版：tests/test_state_machine.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
import pytest
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.core.state_machine import ensure_transition
# [教学注释 L3] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.enums import RunStatus

# [教学注释 L5] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_valid_transition():
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    ensure_transition(RunStatus.CREATED, RunStatus.INPUT_VALIDATING)

# [教学注释 L8] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
def test_invalid_transition():
    # [教学注释 L9] 通过上下文管理器确保资源在离开代码块时被正确释放。
    with pytest.raises(ValueError):
        # [教学注释 L10] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        ensure_transition(RunStatus.CREATED, RunStatus.COMPLETED)
