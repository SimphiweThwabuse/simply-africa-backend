from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from app.models.commitment import DeliveryStatus


class CommitmentOut(BaseModel):
    id: int
    organisation_id: int
    organisation_name: str
    opportunity_id: Optional[int]
    opportunity_title: Optional[str]
    responsible_id: Optional[int]
    description: str
    committed_value: Optional[Decimal]
    due_date: Optional[date]
    delivery_status: DeliveryStatus


class CommitmentList(BaseModel):
    items: list[CommitmentOut]
    total: int
