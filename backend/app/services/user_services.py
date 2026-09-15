from sqlalchemy.orm import Session
from app.models.user import User,Role,UserRole
from app.schemas.user import UserCreate
from app.auth.security import Hash 
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError

class User_Serviices():
    @staticmethod
    def create_user(db: Session, data: UserCreate):
        
        user = User(
            full_name=data.full_name,
            email=data.email,
            password=Hash.hash(data.password),
         
        )
        try:

            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Conflicts: data alreafy exist"
            )


        role_name = "doctor"

        role = db.query(Role).filter(Role.name == role_name).first()

        if role:
            user_role = UserRole(
                user_id = user.id,
                role_id = role.id
            )
            db.add(user_role)
            db.commit()




        return user
    
   