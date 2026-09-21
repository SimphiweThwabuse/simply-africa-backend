from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.organisation import OrgType, OrgStatus, HealthStatus


# Fields the client sends when creating an organisation
class OrganisationCreate(BaseModel):
    name: str
    sector: Optional[str] = None
    org_type: OrgType = OrgType.other
    location: Optional[str] = None
    status: OrgStatus = OrgStatus.prospect
    owner_id: Optional[int] = None


# Fields the client can update - all optional, since PATCH-style partial updates
class OrganisationUpdate(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    org_type: Optional[OrgType] = None
    location: Optional[str] = None
    status: Optional[OrgStatus] = None
    owner_id: Optional[int] = None
    health_status: Optional[HealthStatus] = None


# What the API returns
class OrganisationOut(BaseModel):
    id: int
    name: str
    sector: Optional[str]
    org_type: OrgType
    location: Optional[str]
    status: OrgStatus
    health_status: HealthStatus
    owner_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read directly from the SQLAlchemy model
