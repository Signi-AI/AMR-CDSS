from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.models import media
from sqlalchemy.exc import IntegrityError
from app.schemas.patient import PatientCreate,PatientUpdate
from datetime import date
from sqlalchemy import or_,asc,desc
from app.models.user import UserRole
from fastapi import HTTPException,status
from app.services.storage.storage import delete_upload_file
from .paginationService import PaginationParams



def calc_age(dob:date):
    today=date.today()
    age=today.year-dob.year-((today.month,today.day)>(dob.month,dob.day))
    return age

class Patient_Services():
    @staticmethod
    def create_patient(db: Session, data: PatientCreate,current_user):

        patient=(db.query(Patient).filter(Patient.full_name==data.full_name,
                                        Patient.date_of_birth==data.date_of_birth,
                                        Patient.gender==data.gender).first())
        if patient:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Patient alredy registered")
        patient = Patient(
            full_name=data.full_name,
            patient_code = data.patient_code,
            date_of_birth=data.date_of_birth,
            age=calc_age(data.date_of_birth),
            gender=data.gender,
            created_by=current_user.id,
          
        )
        try:

            db.add(patient)
            db.commit()
            db.refresh(patient)

        except IntegrityError:
            raise HTTPException(
                status_code=400,detail="conflicts: data already exist"
            )
        
        return patient



    @staticmethod
    def list_patient_with_results(db: Session, params: PaginationParams):

        query = db.query(Patient)

        # 1. Apply filtering if search parameter is provided
        if params.search:
            search_terms = f"%{params.search}%"  # Added trailing % for substring matching
            query = query.filter(
                or_(
                    Patient.patient_code.ilike(search_terms),
                    Patient.full_name.ilike(search_terms)
                )
            )

        # 2. Get total count AFTER applying filters, but BEFORE pagination
        total = query.count()

        # 3. Apply sorting
        sort_column = getattr(Patient, params.sort_by, Patient.created_at)
        if params.order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # 4. Apply pagination and fetch results
        result = query.offset(params.offset).limit(params.limit).all()

        return result, total

    @staticmethod
    def update_patient(db: Session, patient_id: int, data: PatientUpdate):
        
                
        patient =db.query(Patient).filter(Patient.id==patient_id).first()
        if not patient:
         raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"patient with id {patient_id} not found")
      
        patient.full_name=data.full_name
        patient.patient_code = data.patient_code
        patient.gender==data.gender
        patient.date_of_birth=data.date_of_birth
        patient.age=calc_age(data.date_of_birth)        
    
        try:

            db.commit()
            db.refresh(patient)
        except InterruptedError:
            raise HTTPException(
                status_code=400,detail="conflict data already exist"
            )
        return patient
    
    @staticmethod
    def delete_patient(db: Session, patient_id: int,current_user):
        if current_user.role != UserRole.ADMIN:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you not have action to perform this")
                
        patient =db.query(Patient).filter(Patient.id==patient_id).first()
        if not patient:
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"patient with id {patient_id} not found")
        db.delete(patient)
        db.commit()
        
        return {
        "message":"patient info deleted"
    }

    #image services
    @staticmethod
    def create_image(patent_id:int,db:Session,path:str):

        patient= db.query(Patient).filter(Patient.id == patent_id).first()

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        image_cover = db.query(media.Media).filter(
            media.Media.id == patient.image_id
        ).first()

        if image_cover:
            image_cover.file_name = path
            delete_upload_file(image_cover.file_path)
            image_cover.file_path = path
            db.commit()
            db.refresh(image_cover)

        else:
            image_cover = media.Media(
                file_name = path,
                file_path = path,

            )

            db.add(image_cover)
            db.flush()
            patient.image_id = image_cover.id

            db.commit()
            db.refresh(image_cover)

            return image_cover









