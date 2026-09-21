from sqlalchemy import Column, Integer, Numeric, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class DeliveryStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    completed = "completed"
    overdue = "overdue"
    cancelled = "cancelled"


class Commitment(Base):
    __tablename__ = "commitments"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="RESTRICT"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="SET NULL"))
    responsible_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    description = Column(Text, nullable=False)
    committed_value = Column(Numeric(14, 2))
    due_date = Column(Date)
    delivery_status = Column(Enum(DeliveryStatus), nullable=False, default=DeliveryStatus.pending)

    organisation = relationship("Organisation", back_populates="commitments")
    opportunity = relationship("Opportunity", back_populates="commitments")
