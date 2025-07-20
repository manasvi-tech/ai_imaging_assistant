from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.models.user import UserRole
from uuid import UUID
from datetime import datetime

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
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    email: Optional[EmailStr] = None  # Add email to update