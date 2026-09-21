from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from app.database import Base
import enum


class ProgrammeStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    completed = "completed"


class Programme(Base):
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(ProgrammeStatus), nullable=False, default=ProgrammeStatus.planned)


class OrgProgramme(Base):
    __tablename__ = "org_programmes"

    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"), primary_key=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), primary_key=True)
    role_in_programme = Column(String(150))
    linked_on = Column(Date)
