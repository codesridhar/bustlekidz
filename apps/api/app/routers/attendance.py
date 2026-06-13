from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.database import get_db
from app.models.attendance import AttendanceRecord, AttendanceStatus

router = APIRouter()


class AttendanceMarkRequest(BaseModel):
    student_id: str
    class_id: str
    date: date
    status: AttendanceStatus
    marked_by: str
    remarks: Optional[str] = None


class AttendanceBulkRequest(BaseModel):
    records: list[AttendanceMarkRequest]


class AttendanceResponse(BaseModel):
    id: str
    student_id: str
    class_id: str
    date: date
    status: AttendanceStatus
    marked_by: str
    remarks: Optional[str]
    whatsapp_sent: bool

    model_config = {"from_attributes": True}


@router.post("/mark", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(data: AttendanceMarkRequest, db: AsyncSession = Depends(get_db)):
    # Prevent duplicate
    existing = await db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.student_id == data.student_id,
            AttendanceRecord.date == data.date,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Attendance already marked for this student today")

    record = AttendanceRecord(**data.model_dump())
    db.add(record)
    await db.flush()
    return record


@router.post("/mark/bulk")
async def mark_bulk_attendance(data: AttendanceBulkRequest, db: AsyncSession = Depends(get_db)):
    created = []
    for item in data.records:
        record = AttendanceRecord(**item.model_dump())
        db.add(record)
        created.append(record.student_id)
    await db.flush()
    return {"marked": len(created), "student_ids": created}


@router.get("/class/{class_id}")
async def get_class_attendance(
    class_id: str,
    attendance_date: date = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    q = select(AttendanceRecord).where(AttendanceRecord.class_id == class_id)
    if attendance_date:
        q = q.where(AttendanceRecord.date == attendance_date)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/student/{student_id}/summary")
async def get_student_attendance_summary(
    student_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AttendanceRecord.status, func.count().label("count"))
        .where(AttendanceRecord.student_id == student_id)
        .group_by(AttendanceRecord.status)
    )
    rows = result.all()
    return {row.status.value: row.count for row in rows}
