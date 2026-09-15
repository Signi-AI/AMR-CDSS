from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient import Patient_Services
from app.auth.auth import get_current_user
from app.models.user import User



router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    return Patient_Services.create_patient(db, data,current_user)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = Patient_Services.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found")
    return patient

@router.get("/", response_model=list[PatientResponse])
def list_patients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return Patient_Services.list_patients(db, skip, limit)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user),
):
    return Patient_Services.update_patient(db,patient_id,data,current_user)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user),
):
    return Patient_Services.delete_patient(db, patient_id,current_user)
        