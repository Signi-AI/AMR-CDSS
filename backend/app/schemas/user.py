from pydantic import BaseModel, EmailStr, field_validator

from datetime import datetime
from typing import Optional,List

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
  

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value


class UserUpdate(BaseModel):
    full_name: Optional[str]=None
    email: Optional[EmailStr]=None
   
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes = True

class Userpagination(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    limit: int
    pages: int
