from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "organisation_id IS NOT NULL OR opportunity_id IS NOT NULL OR commitment_id IS NOT NULL",
            name="chk_task_has_target",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"))
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="CASCADE"))
    commitment_id = Column(Integer, ForeignKey("commitments.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    due_date = Column(Date, nullable=False)
    priority = Column(Enum(Priority), nullable=False, default=Priority.medium)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.open)

    organisation = relationship("Organisation", back_populates="tasks")
