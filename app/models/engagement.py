from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class EngagementType(str, enum.Enum):
    meeting = "meeting"
    call = "call"
    email = "email"
    proposal = "proposal"
    event = "event"
    follow_up = "follow_up"


# Join table for the engagements <-> contacts many-to-many relationship
engagement_participants = Table(
    "engagement_participants",
    Base.metadata,
    Column("engagement_id", Integer, ForeignKey("engagements.id", ondelete="CASCADE"), primary_key=True),
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
)


class Engagement(Base):
    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"), nullable=False)
    logged_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    engagement_type = Column(Enum(EngagementType), nullable=False)
    occurred_at = Column(DateTime, nullable=False)
    summary = Column(Text)
    outcome = Column(Text)
    next_action = Column(Text)
    next_action_date = Column(Date)

    organisation = relationship("Organisation", back_populates="engagements")
    participants = relationship("Contact", secondary=engagement_participants)
