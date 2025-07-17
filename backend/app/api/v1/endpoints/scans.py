from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import magic  # python-magic-bin
from pathlib import Path
from app.schemas.scan import Scan, ScanCreate
from app.services.scan import create_scan, get_scans
from app.db.session import get_db
from app.core.config import settings
from app.db.models.patient import Patient
from app.db.models.scan import Scan as ScanModel
import logging
from uuid import UUID

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed medical image types
ALLOWED_MIME_TYPES = {
    'application/dicom': '.dcm',
    'application/octet-stream': ['.nii', '.nii.gz'],  # NIfTI files
    'image/dicom': '.dcm'  # Alternative DICOM MIME type
}
@router.post("/", response_model=Scan)
async def upload_scan(
    patient_id: str = Form(..., description="ID of the patient as UUID", example="c0391709-40dd-4a50-90c1-0de9851045ed"),
    scan_type: str = Form(..., description="Type of scan (CT, MRI, X-Ray)", example="MRI"),
    file: UploadFile = File(..., description="Medical image file"),
    db: Session = Depends(get_db)
):
    """Upload a medical scan (DICOM/NIfTI)"""
    try:
        # Convert string UUID to UUID object
        try:
            patient_uuid = UUID(patient_id)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid UUID format for patient_id"
            )

        # Verify patient exists
        patient = db.query(Patient).filter(Patient.id == patient_uuid).first()
        if not patient:
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID {patient_id} not found"
            )

        # Validate file type
        file_content = await file.read(2048)
        await file.seek(0)
        
        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type. Allowed: {list(ALLOWED_MIME_TYPES.keys())}"
            )

        # Generate secure file path using absolute path
        UPLOAD_DIR = Path("medical_uploads").absolute()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        ext = ALLOWED_MIME_TYPES[mime_type]
        filename = f"{patient_id}_{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / filename
        
        # Log the file path for debugging
        logger.info(f"Saving file to: {file_path}")

        # Save file with error handling
        try:
            with open(file_path, "wb") as f:
                while content := await file.read(1024 * 1024):  # 1MB chunks
                    f.write(content)
            logger.info(f"Successfully saved file: {filename}")
        except IOError as e:
            logger.error(f"Failed to save file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save uploaded file: {str(e)}"
            )

        # Create database record
        db_scan = ScanModel(
            patient_id=patient_uuid,  # Using the UUID object here
            scan_type=scan_type,
            file_path=str(file_path)  # Store absolute path
        )
        
        try:
            db.add(db_scan)
            db.commit()
            db.refresh(db_scan)
            logger.info(f"Successfully created scan record with ID: {db_scan.id}")
            return db_scan
        except Exception as e:
            db.rollback()
            # Clean up the file if DB operation failed
            if file_path.exists():
                file_path.unlink()
            logger.error(f"Database operation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create scan record: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Scan])
def list_scans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all scans with pagination"""
    try:
        scans = db.query(ScanModel).filter(ScanModel.patient_id != None).offset(skip).limit(limit).all()
        
        # Verify file existence for each scan
        valid_scans = []
        for scan in scans:
            if Path(scan.file_path).exists():
                valid_scans.append(scan)
            else:
                logger.warning(f"File not found for scan ID {scan.id}: {scan.file_path}")
        
        return valid_scans
        
    except Exception as e:
        logger.error(f"Error listing scans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
