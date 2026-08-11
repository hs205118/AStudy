from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.modules import router as modules_router
from app.api.routes.runs import router as runs_router
from app.config import get_settings
from app.infrastructure.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title=get_settings().app_name, version="0.1.0", lifespan=lifespan)
app.include_router(modules_router, prefix="/api/v1")
app.include_router(runs_router, prefix="/api/v1")

@app.get("/health", tags=["system"])
def health(): return {"status": "ok", "environment": get_settings().environment}
