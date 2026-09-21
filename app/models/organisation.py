from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class OrgType(str, enum.Enum):
    sponsor = "sponsor"
    funder = "funder"
    employer = "employer"
    institution = "institution"
    mentor = "mentor"
    speaker = "speaker"
    ecosystem_partner = "ecosystem_partner"
    other = "other"


class OrgStatus(str, enum.Enum):
    prospect = "prospect"
    active = "active"
    dormant = "dormant"
    inactive = "inactive"


class HealthStatus(str, enum.Enum):
    green = "green"
    amber = "amber"
    red = "red"


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sector = Column(String(120))
    org_type = Column(Enum(OrgType), nullable=False, default=OrgType.other)
    location = Column(String(100))  # matches the uploaded schema's single location column
    status = Column(Enum(OrgStatus), nullable=False, default=OrgStatus.prospect)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    health_status = Column(Enum(HealthStatus), nullable=False, default=HealthStatus.amber)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="organisations")
    contacts = relationship("Contact", back_populates="organisation", cascade="all, delete-orphan")
    engagements = relationship("Engagement", back_populates="organisation")
    opportunities = relationship("Opportunity", back_populates="organisation")
    commitments = relationship("Commitment", back_populates="organisation")
    tasks = relationship("Task", back_populates="organisation")
