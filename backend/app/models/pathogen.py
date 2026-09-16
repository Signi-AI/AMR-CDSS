import enum
from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class PathogenFamily(str, enum.Enum):
    GRAM_POSITIVE = "gram_positive"
    GRAM_NEGATIVE = "gram_negative"
    FUNGAL = "fungal"
    VIRAL = "viral"
    OTHER = "other"


class Pathogen(Base):
    __tablename__ = "pathogens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    scientific_name = Column(String(200), nullable=True)
    family = Column(Enum(PathogenFamily), nullable=False)
    description = Column(Text, nullable=True)
    common_resistance_profile = Column(Text, nullable=True)
    is_active = Column(Boolean,default=datetime.now)
    created_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    

    rules= relationship("ClinicalRule",back_populates="pathogen")