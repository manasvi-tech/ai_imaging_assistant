# backend/app/models/patient.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String)
    age = Column(Integer)
    medical_record_num = Column(String)
    reports = relationship("Report", back_populates="patient")
    # Add relationship
    scans = relationship("Scan", back_populates="patient")