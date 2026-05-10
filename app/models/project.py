from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"  # название таблицы в PostgreSQL

    id: Mapped[int] = mapped_column(primary_key=True, index=True) # первичный ключ 1, 2, 3 - уникальный id

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    ) # название проекта string - максимум символов
      # unique=True - нельзя два проекта с одинаковыми названиями
      # nullable=False - обязательное поле

    api_key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    ) # Ключ проекта, будут приходить ошибки и что бы нащ сервер их мог принимать

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ) # дата создания проекта. server_default=func.now() - база сама ставит текущее время

    errors = relationship("Error", back_populates="project")