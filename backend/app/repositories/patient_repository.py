from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from backend.app.models.patient_model import Patient
from backend.app.schemas.patient_schema import PatientCreate


def get_patients(db: Session):
    return db.query(Patient).all()


def create_patient(db: Session, patient: PatientCreate):

    new_patient = Patient(
        document=patient.document,
        full_name=patient.full_name,
        phone=patient.phone
    )

    try:
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        return new_patient

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Document already exists"
        )


def delete_patient(db: Session, patient_id: int):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }


def update_patient(
    db: Session,
    patient_id: int,
    patient_data: PatientCreate
):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient.document = patient_data.document
    patient.full_name = patient_data.full_name
    patient.phone = patient_data.phone

    db.commit()
    db.refresh(patient)

    return patient