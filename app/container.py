from functools import lru_cache
from app.config import get_settings
from app.infrastructure.artifact_store import LocalArtifactStore
from app.services.model_provider import FakeModelProvider
from app.services.module_registry import ModuleRegistry
from app.tools.base import ToolRegistry
from app.tools.builtin import TextStatsTool

@lru_cache
def artifact_store(): return LocalArtifactStore(get_settings().artifact_root)
@lru_cache
def module_registry(): return ModuleRegistry(get_settings().module_root)
@lru_cache
def model_provider(): return FakeModelProvider()
@lru_cache
def tool_registry():
    registry = ToolRegistry(); registry.register(TextStatsTool()); return registry
