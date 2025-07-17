from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import both SQLAlchemy model and Pydantic schemas
from app.db.models.patient import Patient as PatientModel  # SQLAlchemy model
from app.schemas.patient import Patient, PatientCreate  # Pydantic schemas
from app.services.patient import get_patient, get_patients, create_patient
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = get_patients(db, skip=skip, limit=limit)
    return patients

@router.post("/", response_model=Patient)
def create_new_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient=patient)

@router.get("/search/", response_model=List[Patient])
def search_patients(
    name: str = None,
    medical_record_num: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Search patients by name or medical record number (partial matches)
    """
    query = db.query(PatientModel)  # Use SQLAlchemy model here
    
    if name:
        query = query.filter(PatientModel.name.ilike(f"%{name}%"))
    if medical_record_num:
        query = query.filter(PatientModel.medical_record_num.ilike(f"%{medical_record_num}%"))
    
    patients = query.offset(skip).limit(limit).all()
    return patients