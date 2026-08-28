import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.submission import Submission
from app.models.widget import Widget
from app.models.user import User
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdate,
)
from app.services.submission_service import create_submission


router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "/",
    response_model=SubmissionResponse,
    status_code=201,
)
def create_submission_endpoint(
    tenant_id: int,
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied for this tenant",
        )

    widget = (
        db.query(Widget)
        .filter(
            Widget.id == submission_data.widget_id,
            Widget.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=403,
            detail="Widget does not belong to your tenant",
        )

    return create_submission(
        db=db,
        submission_data=submission_data,
        tenant_id=current_user.tenant_id,
    )


@router.get(
    "/",
    response_model=list[SubmissionResponse],
)
def get_submissions_endpoint(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied for this tenant",
        )

    submissions = (
        db.query(Submission)
        .filter(
            Submission.tenant_id == current_user.tenant_id
        )
        .order_by(Submission.created_at.desc())
        .all()
    )

    for submission in submissions:
        submission.data = json.loads(submission.data)

    return submissions


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
def get_submission_endpoint(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = (
        db.query(Submission)
        .filter(
            Submission.id == submission_id,
            Submission.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if submission is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found",
        )

    submission.data = json.loads(submission.data)

    return submission


@router.put(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
def update_submission_endpoint(
    submission_id: int,
    submission_data: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = (
        db.query(Submission)
        .filter(
            Submission.id == submission_id,
            Submission.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if submission is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found",
        )

    submission.data = json.dumps(submission_data.data)

    db.commit()
    db.refresh(submission)

    submission.data = json.loads(submission.data)

    return submission


@router.delete(
    "/{submission_id}",
    status_code=204,
)
def delete_submission_endpoint(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = (
        db.query(Submission)
        .filter(
            Submission.id == submission_id,
            Submission.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if submission is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found",
        )

    db.delete(submission)
    db.commit()

    return None