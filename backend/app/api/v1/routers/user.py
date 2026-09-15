from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.auth.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import User_Serviices


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data:UserCreate, db: Session = Depends(get_db)):
    return User_Serviices.create_user(db, data)
