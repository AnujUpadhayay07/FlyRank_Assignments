from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    users = relationship(
        "User",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    widgets = relationship(
        "Widget",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    submissions = relationship(
        "Submission",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )