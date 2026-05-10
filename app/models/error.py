from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base

class Error(Base):
    __tablename__ = "errors"

    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_groups.id"),
        nullable=True
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    message: Mapped[str] = mapped_column(String(255), nullable=False)

    level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="error"
    )

    stack_trace: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    project = relationship("Project", back_populates="errors")
    group = relationship("ErrorGroup", back_populates="errors")