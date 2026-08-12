"""教学注释版：app/validators/base.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any, Protocol
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.domain.schemas import Finding

# [教学注释 L4] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Validator(Protocol):
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id: str
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version: str
    # [教学注释 L7] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def validate(self, payload: dict[str, Any], context: dict[str, Any]) -> list[Finding]: ...
