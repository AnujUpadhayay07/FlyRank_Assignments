import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class SubmissionCreate(BaseModel):
    widget_id: int
    data: dict


class SubmissionUpdate(BaseModel):
    data: dict


class SubmissionResponse(BaseModel):
    id: int
    tenant_id: int
    widget_id: int
    data: dict
    ip_address: str | None
    country: str | None
    city: str | None
    user_agent: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("data", mode="before")
    @classmethod
    def parse_data(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value