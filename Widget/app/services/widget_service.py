import json
import uuid

from sqlalchemy.orm import Session

from app.models.widget import Widget
from app.schemas.widget import WidgetCreate


def create_widget(
    db: Session,
    widget_data: WidgetCreate,
    tenant_id: int,
) -> Widget:
    widget = Widget(
        tenant_id=tenant_id,
        public_id=str(uuid.uuid4()),
        name=widget_data.name,
        title=widget_data.title,
        description=widget_data.description,
        fields=json.dumps(widget_data.fields),
        button_text=widget_data.button_text,
        version=1,
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return widget