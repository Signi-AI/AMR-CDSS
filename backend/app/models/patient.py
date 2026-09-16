from sqlalchemy import Column, Integer, String, Date, DateTime, Enum,ForeignKey
import enum
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(20), unique=True, index=True, nullable=True)
    full_name = Column(String(150), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    age=Column(Integer,nullable=True)
  
    created_by=Column(Integer,ForeignKey("users.id"))
   
    image_id = Column(Integer,ForeignKey("media.id"))
    created_at = Column(DateTime,default=datetime.now())
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)

    media = relationship("Media",back_populates="patient")
    user=relationship("User",back_populates="patient")
    analysis = relationship("AnalysisResult", back_populates="patient")
    