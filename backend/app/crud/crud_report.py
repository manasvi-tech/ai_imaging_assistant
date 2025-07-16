from sqlalchemy.orm import Session
from app.db.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate
from uuid import UUID

def create_report(db: Session, report_in: ReportCreate, user_id: UUID) -> Report:
    report = Report(**report_in.dict(), created_by=user_id)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_report(db: Session, report_id: UUID) -> Report:
    return db.query(Report).filter(Report.id == report_id).first()

def get_reports_for_patient(db: Session, patient_id: UUID):
    return db.query(Report).filter(Report.patient_id == patient_id).all()

def update_report(db: Session, report_id: UUID, report_in: ReportUpdate):
    report = get_report(db, report_id)
    if not report:
        return None
    for field, value in report_in.dict(exclude_unset=True).items():
        setattr(report, field, value)
    db.commit()
    db.refresh(report)
    return report
