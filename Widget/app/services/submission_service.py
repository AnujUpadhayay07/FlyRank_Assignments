import json

from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate


def create_submission(
    db: Session,
    submission_data: SubmissionCreate,
    tenant_id: int,
    ip_address: str | None = None,
    country: str | None = None,
    city: str | None = None,
    user_agent: str | None = None,
) -> Submission:
    submission = Submission(
        tenant_id=tenant_id,
        widget_id=submission_data.widget_id,
        data=json.dumps(submission_data.data),
        ip_address=ip_address,
        country=country,
        city=city,
        user_agent=user_agent,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission