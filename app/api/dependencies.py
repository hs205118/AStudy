from fastapi import Header, HTTPException
from app.config import get_settings

def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if settings.require_api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
