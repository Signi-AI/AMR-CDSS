from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.analysis_result import AnalysisResultCreate
from app.models.analysis_result import AnalysisResult
from app.models.clinical_visit import ClinicalVisit, VisitStatus
from app.models.patient import Patient
from .paginationService import PaginationParams
from sqlalchemy import or_




class Result_service():
    @staticmethod
    def create_analysis(db:Session,data:AnalysisResultCreate):
        patient=db.query(Patient).filter(Patient.id==data.patient_id).first()
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="patient with that id not found")

        
        result=AnalysisResult(
            patient_id = data.patient_id,
            image_path = data.image_path,
            confidence_score = data.confidence_score,
            detection_summary= data.detection_summary

        )
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
    def list_results_by_visit(db: Session, parms: PaginationParams):
        query= db.query(AnalysisResult)

        if parms.search:
            search_terms = f"%{parms.search}%"
            query = query.filter(
                or_(
                    AnalysisResult.detection_summary.ilike(search_terms)
                )
            )

        total = query.count()

        sort_column = getattr(AnalysisResult, parms.sort_by, AnalysisResult.patient_id)
        if parms.order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        results = query.offset(parms.offset).limit(parms.limit).all()

        return results, total

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