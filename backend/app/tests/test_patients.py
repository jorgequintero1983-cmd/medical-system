from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from backend.app.api.routes import patient_routes
from backend.app.main import app
from backend.app.models.patient_model import Patient
from backend.app.tests.mocks.db_mock import build_mock_db, override_get_db

client = TestClient(app)


@pytest.mark.unitaria
def test_get_patients():
    mock_db = build_mock_db()
    mock_patient = Patient(
        id=1,
        document="1234567890",
        full_name="Paciente Mock",
        phone="3001234567",
    )
    mock_db.query.return_value.all.return_value = [mock_patient]
    app.dependency_overrides[patient_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.get("/patients/")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    mock_db.query.assert_called_with(Patient)


@pytest.mark.unitaria
def test_create_patient():
    mock_db = build_mock_db()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[patient_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/patients/",
            json={
                "document": "9876543210",
                "full_name": "Paciente Test",
                "phone": "3001234567",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["document"] == "9876543210"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.unitaria
def test_duplicate_patient():
    mock_db = build_mock_db()
    existing = MagicMock(spec=Patient)
    existing.document = "5555555555"
    mock_db.query.return_value.filter.return_value.first.return_value = existing
    app.dependency_overrides[patient_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/patients/",
            json={
                "document": "5555555555",
                "full_name": "Paciente Duplicado 2",
                "phone": "3002222222",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Está intentando crear un paciente duplicado"
    )
    mock_db.add.assert_not_called()


@pytest.mark.unitaria
def test_invalid_document():
    mock_db = build_mock_db()
    app.dependency_overrides[patient_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/patients/",
            json={
                "document": "ABC123",
                "full_name": "Paciente Test",
                "phone": "3001234567",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    mock_db.query.assert_not_called()


@pytest.mark.unitaria
def test_invalid_phone():
    mock_db = build_mock_db()
    app.dependency_overrides[patient_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/patients/",
            json={
                "document": "123456789",
                "full_name": "Paciente Test",
                "phone": "ABCDEF",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    mock_db.query.assert_not_called()
