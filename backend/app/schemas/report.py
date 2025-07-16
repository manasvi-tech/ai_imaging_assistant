from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    scan_id: UUID
    patient_id: UUID
    generated_diagnosis: Optional[str] = None
    doctor_notes: Optional[str] = None
    final_report: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    doctor_notes: Optional[str] = None
    final_report: Optional[str] = None

class ReportOut(ReportBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
