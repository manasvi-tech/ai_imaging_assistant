from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    generated_diagnosis = Column(Text, nullable=True)  # From AI
    doctor_notes = Column(Text, nullable=True)         # Editable
    final_report = Column(Text, nullable=True)         # Saved version

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional relationships
    scan = relationship("Scan", back_populates="report")
    patient = relationship("Patient", back_populates="reports")
    author = relationship("User", back_populates="reports")
