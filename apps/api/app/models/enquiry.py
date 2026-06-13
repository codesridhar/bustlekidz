import enum
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class EnquiryStatus(str, enum.Enum):
    NEW = "new"
    VISIT_SCHEDULED = "visit_scheduled"
    VISIT_DONE = "visit_done"
    ADMISSION = "admission"
    DROPPED = "dropped"


class Enquiry(Base):
    __tablename__ = "enquiries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_name: Mapped[str] = mapped_column(String(255), nullable=False)
    child_name: Mapped[str] = mapped_column(String(255), nullable=False)
    child_age_months: Mapped[int | None] = mapped_column(nullable=True)
    program_interest: Mapped[str] = mapped_column(String(50), nullable=False)  # Playgroup, LKG, etc.
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    whatsapp_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="website")  # website, walkin, referral
    status: Mapped[EnquiryStatus] = mapped_column(SAEnum(EnquiryStatus), default=EnquiryStatus.NEW, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
