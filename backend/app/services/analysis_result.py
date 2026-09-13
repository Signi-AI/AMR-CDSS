from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.analysis_result import AnalysisResultCreate
from app.models.analysis_result import AnalysisResult
from app.models.clinical_visit import ClinicalVisit, VisitStatus




class Result_service():
    @staticmethod
    def create_analysis(db:Session,data:AnalysisResultCreate):
        visit=db.query(ClinicalVisit).filter(ClinicalVisit.id==data.visit_id).first()
        if not visit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="clinical visist not found")
        visit.status=VisitStatus.AWAITING_REVIEW
        db.commit()
        db.refresh(visit)
        
        result=AnalysisResult(**data.model_dump())
        db.add(result)
        db.commit()
        db.refresh(result)
        
        return result
    @staticmethod
    def get_analysis_result(db: Session, result_id: int):
        result = db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result not found")
        return result

    @staticmethod
    def list_results_by_visit(db: Session, visit_id: int):
        visit_list= (
            db.query(AnalysisResult)
            .filter(AnalysisResult.visit_id == visit_id)
            .order_by(AnalysisResult.analyzed_at.desc())
            .all()
        )
        return visit_list

    @staticmethod
    def delete_analysis_result(db: Session, result_id: int):
        result = db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="deleted succesful")
        db.delete(result)
        db.commit()
        return {
            "message":"deleted succesfuly"
        }    