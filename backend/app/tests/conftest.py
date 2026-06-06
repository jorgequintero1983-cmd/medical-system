import os

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from backend.app.database.connection import Base, SessionLocal, engine
from backend.app.main import app
from backend.app.models.patient_model import Patient  # noqa: F401
from backend.app.models.user_model import User

ADMIN_PASSWORD_HASH = (
    "$2b$12$AsnHg/.BJ6ESCtyolKS3FOf9/k9.Y2M.vr66ISvLVxJBlWIp4RihO"
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
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
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)
