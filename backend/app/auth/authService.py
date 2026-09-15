from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.security import Hash
from app.auth import jwt_token
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from app.models import user as ModoleUsers


def login(request: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session= Depends(get_db)):

    user = db.query(ModoleUsers.User).filter(ModoleUsers.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Incorrect password or username',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Incorrect password or username',
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User account is inactive. Please contact administrator.'
        )
    
    #  create token
    access_token = jwt_token.create_access_token(data = {
       "sub": str(user.id)
    })
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
