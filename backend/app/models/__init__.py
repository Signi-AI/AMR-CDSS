#import your model here

from app.core.database import Base
from app.models.user import User,UserRole,Role
from app.models.patient import Patient
from app.models.media import Media
from app.models.clinical_visit import ClinicalVisit
from app.models.antinicrobial import Antimicrobial
from app.models.pathogen import Pathogen
from app.models.analysis_result import AnalysisResult




__all__=["Base","User","Patient","Media","ClinicalVisit","Pathogen","Antimicrobial","AnalysisResult","UserRole","Role"]





