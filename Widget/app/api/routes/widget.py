import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.widget import Widget
from app.schemas.widget import WidgetCreate, WidgetResponse
from app.services.widget_service import create_widget


router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"],
)


@router.post(
    "/",
    response_model=WidgetResponse,
    status_code=201,
)
def create_widget_endpoint(
    tenant_id: int,
    widget_data: WidgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this tenant",
        )

    return create_widget(
        db=db,
        widget_data=widget_data,
        tenant_id=current_user.tenant_id,
    )


@router.get(
    "/",
    response_model=list[WidgetResponse],
)
def get_widgets_endpoint(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this tenant",
        )

    widgets = (
        db.query(Widget)
        .filter(
            Widget.tenant_id == current_user.tenant_id
        )
        .all()
    )

    for widget in widgets:
        widget.fields = json.loads(widget.fields)

    return widgets


@router.get(
    "/{public_id}",
    response_model=WidgetResponse,
)
def get_widget_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.public_id == public_id,
            Widget.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    widget.fields = json.loads(widget.fields)

    return widget


@router.put(
    "/{public_id}",
    response_model=WidgetResponse,
)
def update_widget_endpoint(
    public_id: str,
    widget_data: WidgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.public_id == public_id,
            Widget.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    widget.name = widget_data.name
    widget.title = widget_data.title
    widget.description = widget_data.description
    widget.fields = json.dumps(widget_data.fields)
    widget.button_text = widget_data.button_text
    widget.version += 1

    db.commit()
    db.refresh(widget)

    widget.fields = json.loads(widget.fields)

    return widget


@router.delete(
    "/{public_id}",
    status_code=204,
)
def delete_widget_endpoint(
    public_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.public_id == public_id,
            Widget.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    db.delete(widget)
    db.commit()

    return None