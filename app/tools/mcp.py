from typing import Any, Protocol
from app.tools.base import ToolResult

class MCPClient(Protocol):
    def call(self, server_id: str, tool_name: str, arguments: dict[str, Any]) -> ToolResult: ...

class NoopMCPClient:
    def call(self, server_id: str, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        return ToolResult(False, error_code="MCP_NOT_CONFIGURED", error_message=f"MCP server {server_id} is not configured")
