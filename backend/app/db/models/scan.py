from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    file_path = Column(String, nullable=False)
    scan_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    report = relationship("Report", back_populates="scan", uselist=False)
    patient = relationship("Patient", back_populates="scans")
