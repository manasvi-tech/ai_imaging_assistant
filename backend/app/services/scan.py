from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import os
from datetime import datetime
import uuid
from pathlib import Path  # Add this import
from app.db.models.scan import Scan as ScanModel
from app.core.config import settings
from app.schemas.scan import ScanCreate

async def create_scan(db: Session, scan_data: ScanCreate) -> ScanModel:
    """Create a new scan record"""
    try:
        # Convert to absolute path and ensure directory exists
        file_path = Path(scan_data.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        db_scan = ScanModel(
            patient_id=scan_data.patient_id,
            scan_type=scan_data.scan_type,
            file_path=str(file_path)  # Store as string
        )
        db.add(db_scan)
        db.commit()
        db.refresh(db_scan)
        return db_scan
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create scan record: {str(e)}")

def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ScanModel).offset(skip).limit(limit).all()