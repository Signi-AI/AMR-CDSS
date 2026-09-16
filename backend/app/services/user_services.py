from sqlalchemy.orm import Session
from app.models.user import User,Role,UserRole
from app.schemas.user import UserCreate,UserUpdate
from app.auth.security import Hash 
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_,asc,desc
from app.services.paginationService import PaginationParams

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
    
    # @staticmethod
    # def all_user(db:Session):
    #     users=db.query(User).all()
    #     return users
    
    @staticmethod
    def myinfo(db:Session,current_user):
        user=db.query(User).filter(User.id==current_user.id).first()
        return user 
    
    @staticmethod
    def all_user(db: Session, params: PaginationParams):

        user=db.query(User)
        if params.search:
            search_terms = f"%{params.search}%"  # Added trailing % for substring matching
            user= user.filter(
                or_(
                    User.full_name.ilike(search_terms),
                    User.email.ilike(search_terms)
                )
            )
        total = user.count()

        
        sort_column = getattr(User, params.sort_by, User.created_at)
        if params.order == "asc":
            user = user.order_by(sort_column.asc())
        else:
            user = user.order_by(sort_column.desc())

       
        result = user.offset(params.offset).limit(params.limit).all()

        return result, total
    
    
    @staticmethod
    def show_byId(user_id:int,db:Session):
        user=db.query(User).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with ID {user_id} not found")
        return user
    
    @staticmethod
    def update(user_id:int,db:Session,data:UserUpdate,current_user):
        user=db.query(User).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with ID {user_id} not found")
        user_roles = {ur.roles.name for ur in current_user.role if ur.roles}
   
        if "admin" not in user_roles and user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"you not have access to perforn this")
        
        user.full_name=data.full_name
        user.email=data.email
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(user_id:int,db:Session,current_user):
        user=db.query(User).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with ID {user_id} not found")
        user_roles = {ur.roles.name for ur in current_user.role if ur.roles}
   
        if "admin" not in user_roles and user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"you not have access to perforn this")
        db.delete(user)
        db.commit()
        return {"message":"user deleted successfuly"}
            
    
         
    
   