from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class ModuleDefinition:
    id: str
    name: str
    version: str
    raw: dict[str, Any]
    base_path: Path

class ModuleRegistry:
    def __init__(self, root: Path):
        self.root = root

    def list_modules(self) -> list[ModuleDefinition]:
        result = []
        if not self.root.exists():
            return result
        for file in self.root.glob("*/module.yaml"):
            result.append(self._load(file))
        return result

    def get(self, module_id: str, version: str) -> ModuleDefinition:
        # Prevent path traversal; module IDs are resolved by scanning trusted manifests.
        for module in self.list_modules():
            if module.id == module_id and module.version == version:
                return module
        raise KeyError(f"Module not found: {module_id}@{version}")

    def _load(self, file: Path) -> ModuleDefinition:
        raw = yaml.safe_load(file.read_text(encoding="utf-8"))
        data = raw["module"]
        return ModuleDefinition(data["id"], data["name"], data["version"], data, file.parent)

    @staticmethod
    def read_relative(module: ModuleDefinition, relative: str) -> str:
        target = (module.base_path / relative).resolve()
        if module.base_path.resolve() not in target.parents:
            raise ValueError("Unsafe module resource path")
        return target.read_text(encoding="utf-8")
