from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(150), nullable=False)
    job_title = Column(String(150))
    email = Column(String(255))
    mobile = Column(String(30))
    is_primary = Column(Boolean, nullable=False, default=False)
    notes = Column(Text)

    organisation = relationship("Organisation", back_populates="contacts")
