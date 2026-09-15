import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum,ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

"""class UserRole(str, enum.Enum):
    DOCTOR= "doctor"
    LAB_TECHNICIAN = "lab_technician"
    ADMIN = "admin"
    """

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
   
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    visit= relationship("ClinicalVisit",back_populates="user")
    patient=relationship("Patient",back_populates="user")

    role = relationship("UserRole", back_populates="user")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)

    user_role = relationship("UserRole", back_populates="roles")

    


class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("role.id"))


    user = relationship("User", back_populates="role")
    roles = relationship("Role" , back_populates="user_role")



