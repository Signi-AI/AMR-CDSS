from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class CellCount(Base):
    __tablename__ = "cell_counts"

    id = Column(Integer, primary_key=True, index=True)
   
    rbc_count = Column(Float, nullable=True)
    wbc_count = Column(Float, nullable=True)
    platelet_count = Column(Float, nullable=True)
    hemoglobin_level = Column(Float, nullable=True)
    hematocrit = Column(Float, nullable=True)

    created_at = Column(DateTime,default=datetime.max)

   