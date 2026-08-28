from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class TenantCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Tenant name cannot be empty")

        if len(value) > 100:
            raise ValueError("Tenant name must not exceed 100 characters")

        return value


class TenantResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)