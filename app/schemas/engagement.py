from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.engagement import EngagementType


class EngagementCreate(BaseModel):
    organisation_id: int
    engagement_type: EngagementType
    occurred_at: datetime
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[date] = None
    participant_ids: List[int] = []


class EngagementUpdate(BaseModel):
    organisation_id: Optional[int] = None
    engagement_type: Optional[EngagementType] = None
    occurred_at: Optional[datetime] = None
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[date] = None
    participant_ids: Optional[List[int]] = None


class EngagementOut(BaseModel):
    id: int
    organisation_id: int
    organisation_name: str
    engagement_type: EngagementType
    occurred_at: datetime
    summary: Optional[str]
    outcome: Optional[str]
    next_action: Optional[str]
    next_action_date: Optional[date]
    participant_ids: List[int]


class EngagementList(BaseModel):
    items: List[EngagementOut]
    total: int
