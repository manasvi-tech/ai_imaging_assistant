# backend/app/schemas/patient.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PatientBase(BaseModel):
    name: str
    age: int
    medical_record_num: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: UUID = Field(..., example="c0391709-40dd-4a50-90c1-0de9851045ed")
    
    class Config:
        from_attributes = True