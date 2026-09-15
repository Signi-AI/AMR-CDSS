from app.services.ml_services import image_analysis
from app.services.patient import Patient_Services
from fastapi import APIRouter,File,UploadFile,Depends
from app.services.storage.storage import save_upload_file,IMAGE_TYPES,UploadCatgory
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import get_current_user
from app.core.database import get_db
from app.schemas.analysis_result import AnalysisResultCreate,AnalysisResultOut
from app.services.analysis_result import Result_service



router=APIRouter(prefix="/image",tags=["Image analysis"])

@router.post("/{visit_id}")
async def uplaod_image(visit_id,db:Session=Depends(get_db),file:UploadFile=File(...),
                       current_user:User=Depends(get_current_user)):

    image=await file.read()
    analysis=image_analysis(image)

    
    file_path = save_upload_file(
        file=file,
        allowed_types=IMAGE_TYPES,
        category=UploadCatgory.AMR_PHOTO
    )
    
    data=AnalysisResultCreate(
        visit_id=visit_id,
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
                        current_user:User=Depends(get_current_user)):
    
    return Result_service.get_analysis_result(db, result_id)


@router.get("/visit/{visit_id}", response_model=list[AnalysisResultOut])
def get_results_by_visit(visit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return Result_service.list_results_by_visit(db, visit_id)


@router.delete("/{result_id}", status_code=204)
def delete_analysis_result(
    result_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return Result_service.delete_analysis_result(db,result_id)
   
