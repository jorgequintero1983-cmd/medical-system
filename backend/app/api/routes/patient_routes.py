from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.patient_model import Patient
from backend.app.schemas.patient_schema import PatientCreate

router = APIRouter(prefix="/patients", tags=["Patients"])


# =========================
# CONEXIÓN DB
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# LISTAR PACIENTES
# =========================

@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


# =========================
# CREAR PACIENTE
# =========================

@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    # Validar duplicados por documento
    existing_patient = (
        db.query(Patient)
        .filter(Patient.document == patient.document)
        .first()
    )

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Está intentando crear un paciente duplicado"
        )

    new_patient = Patient(
        document=patient.document,
        full_name=patient.full_name,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# =========================
# ELIMINAR PACIENTE
# =========================

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    db.delete(patient)
    db.commit()

    return {"message": "Paciente eliminado"}


# =========================
# EDITAR PACIENTE
# =========================

@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    data: PatientCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    duplicate = (
        db.query(Patient)
        .filter(
            Patient.document == data.document,
            Patient.id != patient_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Ya existe otro paciente con ese documento"
        )

    patient.document = data.document
    patient.full_name = data.full_name
    patient.phone = data.phone

    db.commit()
    db.refresh(patient)

    return patient