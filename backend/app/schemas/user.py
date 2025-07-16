# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.models.user import UserRole
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[UserRole] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID
    role: UserRole
    
    class Config:
        from_attributes = True
