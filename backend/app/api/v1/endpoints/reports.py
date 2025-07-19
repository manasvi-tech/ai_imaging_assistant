from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut
from app.core.security import get_current_user
from app.db.models.user import User
from app.crud import crud_report
from app.core.config import settings
import os
from app.services.ai.segmentation import call_medsam_segmentation
from app.api.utils.image_converter import dicom_to_png
from app.services.ai.gemini_reasoning import analyze_scan_with_gemini
from app.db.models.patient import Patient
from app.db.models.report import Report
import logging

from uuid import uuid4

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/", response_model=ReportOut)
def create_report(report: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_report.create_report(db, report, user_id=current_user.id)

@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: UUID, db: Session = Depends(get_db)):
    report = crud_report.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/{report_id}", response_model=ReportOut)
def update_report(report_id: UUID, report_in: ReportUpdate, db: Session = Depends(get_db)):
    report = crud_report.update_report(db, report_id, report_in)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/segment_scan/{scan_id}", tags=["AI"])
def segment_scan_by_id(scan_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get scan from DB
    scan = crud_report.get_scan_by_id(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    scan_path = scan.file_path
    if not os.path.exists(scan_path):
        raise HTTPException(status_code=404, detail=f"Scan file not found at {scan_path}")

    try:
        # ✅ Fix: Use scan_path instead of undefined image_path
        if scan_path.lower().endswith(".dcm"):
            converted_path = scan_path.replace(".dcm", f"_{uuid4().hex}.png")
            dicom_to_png(scan_path, converted_path)
            image_path = converted_path
        else:
            image_path = scan_path

        # ✅ Now safely call segmentation
        segmentation_result = call_medsam_segmentation(image_path)

        return {
            "scan_id": str(scan.id),
            "segmentation_result": segmentation_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation failed: {str(e)}")
    
    


@router.post("/analyze_scan/{scan_id}", tags=["AI"])
def analyze_scan(scan_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scan = crud_report.get_scan_by_id(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    image_path = scan.file_path
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")

    patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found for scan")

    age = patient.age if patient.age is not None else 60
    scan_type = scan.scan_type or "Unknown"

    if image_path.endswith(".dcm"):
        converted_path = image_path.replace(".dcm", ".png")
        dicom_to_png(image_path, converted_path)
        image_path = converted_path

    try:
        # Call Gemini and get findings
        gemini_summary = analyze_scan_with_gemini(
            image_path=image_path,
            age=age,
            scan_type=scan_type
        )

        # ✅ Save to database in generated_diagnosis only
        report = Report(
            scan_id=scan.id,
            patient_id=patient.id,
            generated_diagnosis=gemini_summary,
            created_by=current_user.id
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        return {
        "scan_id": str(scan.id),
        "report_id": str(report.id),  # Make sure this is returned
        "generated_diagnosis": gemini_summary
    }

    except Exception as e:
        logger.exception("AI reasoning failed.")
        raise HTTPException(status_code=500, detail=f"AI reasoning failed: {str(e)}")
