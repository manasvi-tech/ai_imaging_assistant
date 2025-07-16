from sqlalchemy.orm import Session
from app.db.models.patient import Patient as PatientModel
from app.schemas.patient import PatientCreate

def get_patient(db: Session, patient_id: int):
    return db.query(PatientModel).filter(PatientModel.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PatientModel).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: PatientCreate):
    db_patient = PatientModel(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient