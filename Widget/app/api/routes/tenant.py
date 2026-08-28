from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.tenant import TenantCreate, TenantResponse
from app.services.tenant_service import create_tenant


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


@router.post(
    "/",
    response_model=TenantResponse,
    status_code=201,
)
def create_tenant_endpoint(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
):
    return create_tenant(
        db=db,
        tenant_data=tenant_data,
    )