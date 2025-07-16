from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut
from app.core.security import get_current_user
from app.db.models.user import User
from app.crud import crud_report
from app.services.ai.document_ai import process_scan_with_docai
from app.services.ai.language_ai import extract_medical_entities
from app.core.config import settings

router = APIRouter()

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


@router.post("/generate_ai_report", tags=["AI"])
def generate_ai_report(report_id: UUID, db: Session = Depends(get_db), current=Depends(get_current_user)):
    report = db.query(Report).get(report_id)
    assert report and report.scan and report.patient
    ai_doc = process_scan_with_docai(settings.GCP_PROJECT, "us", settings.DOCAI_PROCESSOR_ID, report.scan.file_path, "image/jpeg")
    entities = extract_medical_entities(ai_doc["text"])
    report.generated_diagnosis = ai_doc["text"]  # or process entities
    db.commit()
    return {"generated_diagnosis": report.generated_diagnosis, "entities": entities}

