from app.services.ml_services import image_analysis
from app.services.patient import Patient_Services
from fastapi import APIRouter,File,UploadFile,Depends,Query
from app.services.storage.storage import save_upload_file,IMAGE_TYPES,UploadCatgory
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import get_current_user
from app.core.database import get_db
from app.schemas.analysis_result import AnalysisResultCreate,AnalysisResultOut,AnalysisPag
from app.services.analysis_result import Result_service
from app.auth.RoleAuth import RoleChecker
from app.services.paginationService import PaginationParams
import math

doctor = RoleChecker(["doctor","admin"])



router=APIRouter(prefix="/image",tags=["Image analysis"])

@router.post("/{patient_id}")
async def uplaod_image(patient_id,db:Session=Depends(get_db),file:UploadFile=File(...),
                       current_user:User=Depends(doctor)):

    image=await file.read()
    analysis=image_analysis(image)

    
    file_path = save_upload_file(
        file=file,
        allowed_types=IMAGE_TYPES,
        category=UploadCatgory.AMR_PHOTO
    )
    
    data=AnalysisResultCreate(
        patient_id=patient_id,
        image_path=file_path,
        detection_summary=",".join(
            item["class_name"]
            for item in analysis),
        confidence_score=None,
    )
    result=Result_service.create_analysis(db,data)
    
    return{
        "filename":file.filename,
        "analysis":analysis,
    } 
    

@router.get("/{result_id}", response_model=AnalysisResultOut)
def get_analysis_result(result_id: int, 
                        db: Session = Depends(get_db), 
                        current_user:User=Depends(doctor)):
    
    return Result_service.get_analysis_result(db, result_id)


@router.get("/", response_model=AnalysisPag)
def get_results_by_visit(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    search: str = Query(default=None),
    sort_by : str = Query(default="patient_id"),
    order : str = Query(default="desc"),
    db: Session = Depends(get_db),
    current_user:User=Depends(doctor),
      ):

    params = PaginationParams(
        page=page,limit=limit,search=search,sort_by=sort_by,order=order
    )
    analysis, total = Result_service.list_results_by_visit(db, params)

    pages = math.ceil(total/ limit) if total > 0 else 0
    return {
        "items": analysis,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }


@router.delete("/{result_id}", status_code=204)
def delete_analysis_result(
    result_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return Result_service.delete_analysis_result(db,result_id)
   
