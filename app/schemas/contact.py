from typing import Optional
from pydantic import BaseModel


class ContactCreate(BaseModel):
    organisation_id: int
    full_name: str
    job_title: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    is_primary: bool = False
    notes: Optional[str] = None


class ContactUpdate(BaseModel):
    organisation_id: Optional[int] = None
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    is_primary: Optional[bool] = None
    notes: Optional[str] = None


class ContactOut(ContactCreate):
    id: int

    class Config:
        from_attributes = True
