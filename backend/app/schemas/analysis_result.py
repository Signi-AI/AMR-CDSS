from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from typing import List


class AnalysisResultCreate(BaseModel):
    patient_id: int
    image_path: str
    confidence_score: Optional[float] = None
    detection_summary: Optional[str] = None

    @field_validator("confidence_score")
    @classmethod
    def score_in_range(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (0.0 <= value <= 1.0):
            raise ValueError("confidence_score must be between 0.0 and 1.0")
        return value


class AnalysisResultOut(BaseModel):
    id: Optional[int] = None
    patient_id: int
    image_path: str
    confidence_score: Optional[float] = None
    detection_summary: Optional[str] = None
    analyzed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class AnalysisPag(BaseModel):
    items: List[AnalysisResultOut]
    total: int
    page: int
    limit: int
    pages: int
