from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    profile_picture: Optional[str]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
