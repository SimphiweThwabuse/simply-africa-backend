from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from app.models.opportunity import OpportunityStage, OpportunityType


class OpportunityCreate(BaseModel):
    organisation_id: int
    title: str
    opportunity_type: OpportunityType = OpportunityType.other
    stage: OpportunityStage = OpportunityStage.lead
    estimated_value: Optional[Decimal] = None
    currency: str = "ZAR"
    expected_decision_date: Optional[date] = None
    next_action: Optional[str] = None


class OpportunityUpdate(BaseModel):
    organisation_id: Optional[int] = None
    title: Optional[str] = None
    opportunity_type: Optional[OpportunityType] = None
    stage: Optional[OpportunityStage] = None
    estimated_value: Optional[Decimal] = None
    currency: Optional[str] = None
    expected_decision_date: Optional[date] = None
    next_action: Optional[str] = None


class OpportunityOut(OpportunityCreate):
    id: int
    owner_id: Optional[int]
    created_at: datetime
    organisation_name: str


class OpportunityList(BaseModel):
    items: list[OpportunityOut]
    total: int
