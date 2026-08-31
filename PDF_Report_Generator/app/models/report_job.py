from sqlalchemy import Column, String, DateTime
from datetime import datetime

from app.db.database import Base


class ReportJob(Base):
    __tablename__ = "report_jobs"

    id = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)