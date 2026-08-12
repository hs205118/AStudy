"""教学注释版：app/tools/base.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from dataclasses import dataclass, field
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any, Protocol

# [教学注释 L4] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@dataclass
# [教学注释 L5] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ToolContext:
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    run_id: str
    # [教学注释 L7] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    module_id: str
    # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    permissions: set[str] = field(default_factory=set)

# [教学注释 L10] 装饰器在函数或类创建时附加框架行为，例如注册路由或声明响应模型。
@dataclass
# [教学注释 L11] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ToolResult:
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    ok: bool
    # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    data: dict[str, Any] = field(default_factory=dict)
    # [教学注释 L14] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    error_code: str | None = None
    # [教学注释 L15] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    error_message: str | None = None

# [教学注释 L17] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class Tool(Protocol):
    # [教学注释 L18] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id: str
    # [教学注释 L19] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version: str
    # [教学注释 L20] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def execute(self, arguments: dict[str, Any], context: ToolContext) -> ToolResult: ...

# [教学注释 L22] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class ToolRegistry:
    # [教学注释 L23] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def __init__(self):
        # [教学注释 L24] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self._tools: dict[str, Tool] = {}
    # [教学注释 L25] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def register(self, tool: Tool) -> None:
        # [教学注释 L26] 把依赖或运行状态保存到当前对象，供其他方法复用。
        self._tools[f"{tool.id}@{tool.version}"] = tool
    # [教学注释 L27] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def get(self, tool_id: str, version: str) -> Tool:
        # [教学注释 L28] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return self._tools[f"{tool_id}@{version}"]
