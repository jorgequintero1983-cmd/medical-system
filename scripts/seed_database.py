"""Crea tablas y usuario admin para pruebas E2E y performance."""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from backend.app.database.connection import Base, SessionLocal, engine
from backend.app.models.patient_model import Patient  # noqa: F401
from backend.app.models.user_model import User

ADMIN_PASSWORD_HASH = (
    "$2b$12$AsnHg/.BJ6ESCtyolKS3FOf9/k9.Y2M.vr66ISvLVxJBlWIp4RihO"
)


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@test.com").first():
            db.add(
                User(
                    username="admin",
                    email="admin@test.com",
                    hashed_password=ADMIN_PASSWORD_HASH,
                    role="admin",
                )
            )
            db.commit()
            print("Usuario admin@test.com creado.")
        else:
            print("Usuario admin@test.com ya existe.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
