from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass
class ToolContext:
    run_id: str
    module_id: str
    permissions: set[str] = field(default_factory=set)

@dataclass
class ToolResult:
    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error_code: str | None = None
    error_message: str | None = None

class Tool(Protocol):
    id: str
    version: str
    def execute(self, arguments: dict[str, Any], context: ToolContext) -> ToolResult: ...

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    def register(self, tool: Tool) -> None:
        self._tools[f"{tool.id}@{tool.version}"] = tool
    def get(self, tool_id: str, version: str) -> Tool:
        return self._tools[f"{tool_id}@{version}"]
