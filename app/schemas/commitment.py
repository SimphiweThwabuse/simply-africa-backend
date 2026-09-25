from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from app.models.commitment import DeliveryStatus

class CommitmentCreate(BaseModel):
    organisation_id: int
    opportunity_id: Optional[int] = None
    responsible_id: Optional[int] = None
    description: str
    committed_value: Optional[Decimal] = None
    due_date: Optional[date] = None
    delivery_status: DeliveryStatus = DeliveryStatus.pending


class CommitmentUpdate(BaseModel):
    organisation_id: Optional[int] = None
    opportunity_id: Optional[int] = None
    responsible_id: Optional[int] = None
    description: Optional[str] = None
    committed_value: Optional[Decimal] = None
    due_date: Optional[date] = None
    delivery_status: Optional[DeliveryStatus] = None


class CommitmentOut(BaseModel):
    id: int
    organisation_id: int
    organisation_name: str
    opportunity_id: Optional[int]
    opportunity_title: Optional[str]
    responsible_id: Optional[int]
    responsible_name: Optional[str]
    description: str
    committed_value: Optional[Decimal]
    due_date: Optional[date]
    delivery_status: DeliveryStatus


class CommitmentList(BaseModel):
    items: list[CommitmentOut]
    total: int
