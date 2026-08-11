from pathlib import Path
from app.tools.base import ToolContext, ToolResult

class TextStatsTool:
    id = "text-stats"
    version = "1.0.0"
    def execute(self, arguments: dict, context: ToolContext) -> ToolResult:
        text = str(arguments.get("text", ""))
        return ToolResult(True, {"characters": len(text), "lines": len(text.splitlines()), "words": len(text.split())})

class FileExistsTool:
    id = "file-exists"
    version = "1.0.0"
    def execute(self, arguments: dict, context: ToolContext) -> ToolResult:
        # Demo only. Production should enforce an allowlisted workspace root.
        path = Path(str(arguments.get("path", "")))
        return ToolResult(True, {"exists": path.exists()})
