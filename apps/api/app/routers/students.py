from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.database import get_db
from app.models.student import Student

router = APIRouter()


class StudentCreate(BaseModel):
    admission_number: str
    full_name: str
    date_of_birth: date
    gender: str
    class_id: Optional[str] = None
    section_id: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    city: str = "Chennai"
    state: str = "Tamil Nadu"


class StudentResponse(BaseModel):
    id: str
    admission_number: str
    full_name: str
    date_of_birth: date
    gender: str
    class_id: Optional[str]
    section_id: Optional[str]

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[StudentResponse])
async def list_students(
    class_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    q = select(Student).where(Student.deleted_at.is_(None))
    if class_id:
        q = q.where(Student.class_id == class_id)
    if search:
        q = q.where(Student.full_name.ilike(f"%{search}%"))
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    student = Student(**data.model_dump())
    db.add(student)
    await db.flush()
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id, Student.deleted_at.is_(None)))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/count/total")
async def student_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count()).select_from(Student).where(Student.deleted_at.is_(None)))
    return {"total": result.scalar()}
