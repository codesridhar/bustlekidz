import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Playgroup, LKG, UKG, Daycare
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # PG, LKG, UKG, DC
    age_min_months: Mapped[int] = mapped_column(Integer, nullable=False)  # 18 for Playgroup
    age_max_months: Mapped[int] = mapped_column(Integer, nullable=False)  # 72 for UKG
    capacity: Mapped[int] = mapped_column(Integer, default=25)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(10), nullable=False)  # A, B, C
    class_id: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
