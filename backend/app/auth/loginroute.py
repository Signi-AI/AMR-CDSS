from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  
from app.core.database import get_db
from typing import Annotated
from app.auth import authService as authentication
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["authentication"])

@router.post("/login")
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], database: Session = Depends(get_db)):
    return authentication.login(request, database)

