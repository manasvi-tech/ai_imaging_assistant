from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.patient import Patient, PatientCreate
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