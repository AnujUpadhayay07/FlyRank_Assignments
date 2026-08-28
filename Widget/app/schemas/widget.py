import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WidgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    fields: list[dict] = Field(min_length=1)
    button_text: str = Field(default="Submit", max_length=100)


class WidgetResponse(BaseModel):
    id: int
    tenant_id: int
    public_id: str
    name: str
    title: str
    description: str | None
    fields: list[dict]
    button_text: str
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("fields", mode="before")
    @classmethod
    def parse_fields(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value