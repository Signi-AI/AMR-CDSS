from fastapi import Depends,HTTPException,status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.auth import jwt_token
from sqlalchemy.orm import Session
from app.core.database import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return jwt_token.verify_token(token, credentials_exception, db)

