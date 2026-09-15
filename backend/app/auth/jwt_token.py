import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt
from app.auth import jwtschema
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.models import user as modeluser
from app.core.config import settings


load_dotenv()

SECRET_KEY = (settings.SECRET_KEY)
ALGORITHM = (settings.ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = (settings.ACCESS_TOKEN_EXPIRE_MINUTES)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str,credentials_exception,db:Session):
   try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = jwtschema.TokenData(email=user_id)
   except InvalidTokenError:
        raise credentials_exception
   user = db.query(modeluser.User).filter(modeluser.User.id == int(user_id)).first()

   if user is None:
        raise credentials_exception

   if not user.is_active:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

   return user