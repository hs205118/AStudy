from typing import Any, Protocol
import re

class ModelProvider(Protocol):
    def structured_extract(self, *, system_prompt: str, user_content: str, schema: dict[str, Any]) -> dict[str, Any]: ...
    def semantic_validate(self, *, source: str, candidate: dict[str, Any]) -> list[dict[str, Any]]: ...

class FakeModelProvider:
    """可离线运行的开发 Provider。生产环境应替换为企业 Model Gateway。"""
    def structured_extract(self, *, system_prompt: str, user_content: str, schema: dict[str, Any]) -> dict[str, Any]:
        raid = re.findall(r"RAID\s*([0-9]+)", user_content, re.I)
        drives = re.findall(r"(\d+)\s*(?:NVMe|drives?|disks?)", user_content, re.I)
        return {
            "ir_version": "1.0",
            "requirements": [{
                "id": "REQ-001",
                "text": user_content.strip() or "No textual requirement supplied",
                "type": "storage",
                "status": "extracted",
                "source": {"artifact_id": "inline", "location": "input_text"},
                "confidence": 0.85
            }],
            "entities": {
                "raid_levels": sorted(set(raid)),
                "drive_count": int(drives[0]) if drives else None
            },
            "conflicts": [],
            "missing_items": [] if user_content.strip() else ["input_text"]
        }

    def semantic_validate(self, *, source: str, candidate: dict[str, Any]) -> list[dict[str, Any]]:
        if not candidate.get("requirements"):
            return [{"rule_id": "ai.requirement.coverage", "severity": "error", "message": "No requirements generated"}]
        return []
