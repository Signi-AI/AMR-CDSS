import enum
from sqlalchemy import Column, Integer, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class VisitStatus(str, enum.Enum):
    PENDING_ANALYSIS = "pending_analysis"
    AWAITING_REVIEW = "awaiting_review"
    CONFIRMED = "confirmed"
    CLOSED = "closed"


class ClinicalVisit(Base):
    __tablename__ = "clinical_visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    physician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    visit_date = Column(DateTime,default=datetime.now)
    symptoms = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    status = Column(Enum(VisitStatus), nullable=False, default=VisitStatus.PENDING_ANALYSIS)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime,default=datetime.now)
    updated_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)

    patient = relationship("Patient", backref="visits")
    user= relationship("User", foreign_keys=[physician_id],back_populates="visit")
    
    