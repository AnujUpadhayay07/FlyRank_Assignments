from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate


def create_tenant(
    db: Session,
    tenant_data: TenantCreate,
) -> Tenant:

    existing_tenant = (
        db.query(Tenant)
        .filter(Tenant.name == tenant_data.name)
        .first()
    )

    if existing_tenant is not None:
        raise HTTPException(
            status_code=409,
            detail="Tenant name already registered",
        )

    tenant = Tenant(
        name=tenant_data.name,
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant