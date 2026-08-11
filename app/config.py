from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="TRD_", extra="ignore")
    app_name: str = "TRD Agent Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./data/trd_agent.db"
    artifact_root: Path = Path("./data/artifacts")
    module_root: Path = Path("./modules")
    max_repair_attempts: int = 2
    require_api_key: bool = False
    api_key: str = "replace-me"

@lru_cache
def get_settings() -> Settings:
    return Settings()
