from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import get_db
from app.models.patient import Patient, Gender
from app.models.clinical_visit import ClinicalVisit, VisitStatus
from app.models.analysis_result import AnalysisResult
from app.models.pathogen import Pathogen
from app.models.antinicrobial import Antimicrobial
from app.models.ckinical_rule import ClinicalRule
from app.models.user import User, UserRole
from app.core.dependencies import get_current_user
from app.services.ml_services import image_analysis
from app.services.storage.storage import save_upload_file, IMAGE_TYPES, UploadCatgory

router = APIRouter(prefix="/workflow", tags=["Workflow"])

def calc_dob_from_age(age: int) -> date:
    return date.today() - timedelta(days=age * 365)

@router.post("/analyze")
async def analyze_sample_workflow(
    patientId: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    disease: str = Form(...),
    medicine_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Patient matching or creation
    # For demo simplicity, try to find patient by patient_code, else by full_name = patientId, else create.
    patient = db.query(Patient).filter(Patient.patient_code == patientId).first()
    if not patient:
        patient = db.query(Patient).filter(Patient.full_name == patientId).first()
        
    if not patient:
        # Create new patient
        try:
            gender_enum = Gender(sex.lower())
        except ValueError:
            gender_enum = Gender.OTHER
            
        patient = Patient(
            patient_code=patientId,
            full_name=patientId, # using ID as name for demo
            date_of_birth=calc_dob_from_age(age),
            age=age,
            gender=gender_enum,
            created_by=current_user.id
        )
        db.add(patient)
        db.flush() 
    
    # 2. Clinical Visit
    visit = ClinicalVisit(
        patient_id=patient.id,
        physician_id=current_user.id,
        diagnosis=disease,
        status=VisitStatus.CONFIRMED
    )
    db.add(visit)
    db.flush()
    
    # 3. Analyze Image
    image_bytes = await file.read()
    analysis_predictions = image_analysis(image_bytes)
    
    file_path = save_upload_file(
        file=file,
        allowed_types=IMAGE_TYPES,
        category=UploadCatgory.AMR_PHOTO
    )
    
    # 4. Map Pathogen
    # Top prediction
    top_prediction = analysis_predictions[0] if analysis_predictions else None
    detected_pathogen = None
    if top_prediction:
        class_name = top_prediction["class_name"]
        detected_pathogen = db.query(Pathogen).filter(Pathogen.name.ilike(f"%{class_name}%")).first()
    
    # 5. Analysis Result
    pathogen_id = detected_pathogen.id if detected_pathogen else None
    result = AnalysisResult(
        visit_id=visit.id,
        pathogen_id=pathogen_id,
        image_path=file_path,
        confidence_score=top_prediction["confidence"] if top_prediction else None,
        detection_summary=",".join(p["class_name"] for p in analysis_predictions)
    )
    db.add(result)
    
    # 6. Clinical Rules
    recommendation_text = "No specific clinical rule found."
    risk_level = "High" 
    treatment_effectiveness = "Resistant"
    
    if detected_pathogen:
        rule = db.query(ClinicalRule).filter(
            ClinicalRule.pathogen_id == detected_pathogen.id,
            ClinicalRule.antimicrobial_id == medicine_id,
            ClinicalRule.is_active == True
        ).first()
        
        if rule:
            recommendation_text = rule.recommendation
            # map severity to risk/effectiveness for frontend
            if rule.severity.value == "critical":
                risk_level = "High"
                treatment_effectiveness = "Resistant"
            elif rule.severity.value == "warning":
                risk_level = "Medium"
                treatment_effectiveness = "Intermediate"
            else: # info
                risk_level = "Low"
                treatment_effectiveness = "Susceptible"
        else:
            # Fallback if no rule exists but we detected something
            recommendation_text = f"Pathogen {detected_pathogen.name} detected, but no specific rule for this medicine."
            
    db.commit()
    
    return {
        "visit_id": visit.id,
        "patient_id": patient.id,
        "analysis": analysis_predictions,
        "recommendation": {
            "treatmentEffectiveness": treatment_effectiveness,
            "adverseReactionRisk": risk_level,
            "message": recommendation_text
        }
    }
