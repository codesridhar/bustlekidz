import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), unique=True, nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    qualification: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specialisation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_of_joining: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_class_teacher: Mapped[bool] = mapped_column(Boolean, default=False)
    assigned_class_id: Mapped[str | None] = mapped_column(String, ForeignKey("classes.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
