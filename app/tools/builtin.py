"""教学注释版：app/tools/builtin.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from pathlib import Path
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.tools.base import ToolContext, ToolResult

# [教学注释 L4] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class TextStatsTool:
    # [教学注释 L5] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id = "text-stats"
    # [教学注释 L6] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version = "1.0.0"
    # [教学注释 L7] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def execute(self, arguments: dict, context: ToolContext) -> ToolResult:
        # [教学注释 L8] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        text = str(arguments.get("text", ""))
        # [教学注释 L9] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return ToolResult(True, {"characters": len(text), "lines": len(text.splitlines()), "words": len(text.split())})

# [教学注释 L11] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class FileExistsTool:
    # [教学注释 L12] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    id = "file-exists"
    # [教学注释 L13] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
    version = "1.0.0"
    # [教学注释 L14] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def execute(self, arguments: dict, context: ToolContext) -> ToolResult:
        # Demo only. Production should enforce an allowlisted workspace root.
        # [教学注释 L16] 执行当前步骤；其作用应结合所在函数的职责和上下游调用关系理解。
        path = Path(str(arguments.get("path", "")))
        # [教学注释 L17] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return ToolResult(True, {"exists": path.exists()})
