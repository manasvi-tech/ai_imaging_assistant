# backend/app/schemas/scan.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ScanBase(BaseModel):
    patient_id: UUID = Field(..., example="c0391709-40dd-4a50-90c1-0de9851045ed")
    scan_type: str

class ScanCreate(ScanBase):
    file_path: str

class Scan(ScanBase):
    id: UUID
    created_at: datetime
    file_path: str
    
    class Config:
        from_attributes = True