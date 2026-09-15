from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse,Patientpagination
from app.services.patient import Patient_Services
from app.auth.auth import get_current_user
from app.models.user import User
from app.auth.RoleAuth import RoleChecker
from typing import Optional
from app.services.paginationService import PaginationParams
import math



admin = RoleChecker(["admin"])
doctor = RoleChecker(["doctor","admin"])



router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(doctor)
):
    return Patient_Services.create_patient(db, data,current_user)



@router.get("/", response_model=Patientpagination)
def list_patients(
    page: int = Query(default=1, ge=1),
    limit : int = Query(default=20, ge=1, le=100),
    search : Optional[str] = Query(default=None),
    sort_by : str = Query(default="created_at"),
    order: str = Query(default="desc"),
    current_user:User=Depends(doctor),
     db: Session = Depends(get_db)
     ):

    params = PaginationParams(
        page=page,limit=limit,search=search,sort_by=sort_by,order=order
    )
    patients, total = Patient_Services.list_patient_with_results(db, params)

    pages = math.ceil(total / limit) if total > 0 else 0
    

    
    return {
            "items": patients,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }

@router.put("/{patient_id}", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def update_patient(
    patient_id: int,
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(doctor),
):
    return Patient_Services.update_patient(db,patient_id,data)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user),
):
    return Patient_Services.delete_patient(db, patient_id,current_user)
        