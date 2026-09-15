from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.auth.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse,UserUpdate
from app.services.user_services import User_Serviices
from app.auth.RoleAuth import RoleChecker

admin_required=RoleChecker(["admin"])
doctor_required=RoleChecker(["admin","doctor"])

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data:UserCreate, db: Session = Depends(get_db)):
    return User_Serviices.create_user(db, data)

@router.get("/", response_model=UserResponse)
def all_user(db:Session=Depends(get_db),
            current_user:User=Depends(admin_required)):
    return User_Serviices.all_user(db)

@router.get("/me", response_model=UserResponse)
def myinfo(db:Session=Depends(get_db),
             current_user:User=Depends(get_current_user)):
    return User_Serviices.myinfo(db,current_user)

@router.get("/{user_id}", response_model=UserResponse)            
def singleuser(user_id:int,db:Session=Depends(get_db),
             current_user:User=Depends(doctor_required)):
    return User_Serviices.show_byId(user_id,db)

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id:int,data:UserUpdate,
           db:Session=Depends(get_db),
            current_user:User=Depends(doctor_required)):
    return User_Serviices.update(user_id,db,data)

@router.delete("/{user_id}")
def delete(user_id:int,db:Session=Depends(get_db)
             ,current_user:User=Depends(doctor_required)):
    return User_Serviices.delete(user_id,db)

