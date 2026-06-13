from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import get_db
from app.models.enquiry import Enquiry, EnquiryStatus

router = APIRouter()


class EnquiryCreate(BaseModel):
    parent_name: str
    child_name: str
    child_age_months: Optional[int] = None
    program_interest: str
    phone: str
    email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = None
    source: str = "website"


class EnquiryResponse(BaseModel):
    id: str
    parent_name: str
    child_name: str
    program_interest: str
    phone: str
    status: EnquiryStatus

    model_config = {"from_attributes": True}


@router.post("/", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_enquiry(data: EnquiryCreate, db: AsyncSession = Depends(get_db)):
    enquiry = Enquiry(**data.model_dump())
    db.add(enquiry)
    await db.flush()
    return enquiry


@router.get("/", response_model=list[EnquiryResponse])
async def list_enquiries(
    enquiry_status: Optional[EnquiryStatus] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    q = select(Enquiry)
    if enquiry_status:
        q = q.where(Enquiry.status == enquiry_status)
    q = q.order_by(Enquiry.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.patch("/{enquiry_id}/status")
async def update_enquiry_status(
    enquiry_id: str,
    new_status: EnquiryStatus,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Enquiry).where(Enquiry.id == enquiry_id))
    enquiry = result.scalar_one_or_none()
    if not enquiry:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Enquiry not found")
    enquiry.status = new_status
    await db.flush()
    return {"id": enquiry_id, "status": new_status}
