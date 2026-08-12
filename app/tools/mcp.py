"""教学注释版：app/tools/mcp.py。注释解释本文件每个主要语句的意图，不改变运行逻辑。"""
# [教学注释 L1] 导入本行后续代码依赖的类型、框架或标准库能力。
from typing import Any, Protocol
# [教学注释 L2] 导入本行后续代码依赖的类型、框架或标准库能力。
from app.tools.base import ToolResult

# [教学注释 L4] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class MCPClient(Protocol):
    # [教学注释 L5] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def call(self, server_id: str, tool_name: str, arguments: dict[str, Any]) -> ToolResult: ...

# [教学注释 L7] 定义一个职责明确的类型，用于封装数据结构、协议或业务能力。
class NoopMCPClient:
    # [教学注释 L8] 定义可复用函数；参数是输入契约，返回值是调用方可消费的结果。
    def call(self, server_id: str, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        # [教学注释 L9] 将本阶段结果返回给调用方，不继续在当前层处理后续职责。
        return ToolResult(False, error_code="MCP_NOT_CONFIGURED", error_message=f"MCP server {server_id} is not configured")
