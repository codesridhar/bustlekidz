import enum
import uuid
from datetime import datetime, date
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    HOLIDAY = "holiday"


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        Index("ix_attendance_student_date", "student_id", "date"),
        Index("ix_attendance_class_date", "class_id", "date"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(String, ForeignKey("students.id"), nullable=False)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("classes.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[AttendanceStatus] = mapped_column(SAEnum(AttendanceStatus), nullable=False)
    marked_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    whatsapp_sent: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
