from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer,ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True)
    image_path = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=True)
    detection_summary = Column(Text, nullable=True)

    analyzed_at = Column(DateTime,default=datetime.now())
    created_at = Column(DateTime,default=datetime.now,onupdate=datetime.now())

    patient = relationship("Patient",back_populates="analysis")
   
    