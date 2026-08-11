from fastapi import APIRouter, Depends
from app.api.dependencies import require_api_key
from app.container import module_registry
router = APIRouter(prefix="/modules", tags=["modules"], dependencies=[Depends(require_api_key)])

@router.get("")
def list_modules():
    return [{"id": m.id, "name": m.name, "version": m.version, "category_id": m.raw.get("category_id")} for m in module_registry().list_modules()]
