from pathlib import Path
from app.services.module_registry import ModuleRegistry

def test_load_storage_module():
    registry = ModuleRegistry(Path("modules"))
    module = registry.get("storage-wizard", "1.0.0")
    assert module.name == "Storage Wizard TRD Parser"
