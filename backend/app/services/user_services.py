from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import Hash 
from fastapi import HTTPException,status

class User_Serviices():
    @staticmethod
    def create_user(db: Session, data: UserCreate):
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "Email already registered")
        user = User(
            full_name=data.full_name,
            email=data.email,
            password=Hash.hash(data.password),
         
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
   