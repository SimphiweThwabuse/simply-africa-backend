from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Text, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class OpportunityType(str, enum.Enum):
    sponsorship = "sponsorship"
    funding = "funding"
    employment = "employment"
    mentorship = "mentorship"
    technology = "technology"
    other = "other"


class OpportunityStage(str, enum.Enum):
    lead = "lead"
    contacted = "contacted"
    proposal = "proposal"
    negotiation = "negotiation"
    won = "won"
    lost = "lost"
    active = "active"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="RESTRICT"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String(255), nullable=False)
    opportunity_type = Column(Enum(OpportunityType), nullable=False)
    stage = Column(Enum(OpportunityStage), nullable=False, default=OpportunityStage.lead)
    estimated_value = Column(Numeric(14, 2))
    currency = Column(String(3), nullable=False, default="ZAR")
    expected_decision_date = Column(Date)
    next_action = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    organisation = relationship("Organisation", back_populates="opportunities")
    commitments = relationship("Commitment", back_populates="opportunity")
