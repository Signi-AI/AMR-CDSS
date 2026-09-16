from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from typing import List,Optional
import math
from app.auth.auth import get_current_user
from app.schemas.user import UserCreate, UserResponse,UserUpdate,Userpagination
from app.services.user_services import User_Serviices
from app.services.paginationService import PaginationParams,PaginatedResponse
from app.auth.RoleAuth import RoleChecker

admin_required=RoleChecker(["admin"])
doctor_required=RoleChecker(["admin","doctor"])

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data:UserCreate, db: Session = Depends(get_db)):
    return User_Serviices.create_user(db, data)

@router.get("/", response_model=Userpagination)
def all_user(
    page: int = Query(default=1, ge=1),
    limit : int = Query(default=20, ge=1, le=100),
    search : Optional[str] = Query(default=None),
    sort_by : str = Query(default="created_at"),
    order: str = Query(default="desc"),
    current_user:User=Depends(admin_required),
     db: Session = Depends(get_db)
     ):

    params = PaginationParams(
        page=page,limit=limit,search=search,sort_by=sort_by,order=order
    )
    users, total =User_Serviices.all_user(db, params)

    pages = math.ceil(total / limit) if total > 0 else 0
    return {
            "items": users,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }

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
    return User_Serviices.update(user_id,db,data,current_user)

@router.delete("/{user_id}")
def delete(user_id:int,db:Session=Depends(get_db)
             ,current_user:User=Depends(doctor_required)):
    return User_Serviices.delete(user_id,db,current_user)

