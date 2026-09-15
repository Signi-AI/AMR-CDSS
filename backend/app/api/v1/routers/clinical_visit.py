from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.clinical_visit import (
    ClinicalVisitCreate,
    ClinicalVisitDiagnosisUpdate,
    ClinicalVisitAssignPhysician,
    ClinicalVisitOut,
)
from app.models.clinical_visit import VisitStatus
from app.services import clinical_visit
from app.auth.auth import get_current_user
from app.models.user import UserRole,User

router = APIRouter(prefix="/clinical-visits", tags=["Clinical Visits"])


@router.post("/", response_model=ClinicalVisitOut, status_code=201)
def create_visit(
    data: ClinicalVisitCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)):

    return clinical_visit.create_visit(db, current_user,data)


@router.get("/{visit_id}", response_model=ClinicalVisitOut)
def get_visit(visit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return clinical_visit.get_visit(db, visit_id)


@router.get("/patient/{patient_id}", response_model=list[ClinicalVisitOut])
def get_visits_by_patient(patient_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return clinical_visit.list_visits_by_patient(db, patient_id)


@router.get("/", response_model=list[ClinicalVisitOut])
def list_visits(
    status: VisitStatus | None = Query(default=None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return clinical_visit.list_visits_by_status(db, status, skip, limit)

@router.patch("/{visit_id}/diagnosis", response_model=ClinicalVisitOut)
def submit_diagnosis(
    visit_id: int,
    data: ClinicalVisitDiagnosisUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    return clinical_visit.submit_diagnosis(db, visit_id, data)


@router.patch("/{visit_id}/close", response_model=ClinicalVisitOut)
def close_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return clinical_visit.close_visit(db, visit_id)