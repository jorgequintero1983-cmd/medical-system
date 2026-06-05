from fastapi.testclient import TestClient
from app.main import app
import random

client = TestClient(app)


def test_get_patients():

    response = client.get("/patients/")

    assert response.status_code == 200


def test_create_patient():

    document = str(random.randint(100000000, 999999999))

    response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Test",
            "phone": "3001234567"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document"] == document


def test_duplicate_patient():

    document = str(random.randint(100000000, 999999999))

    client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Duplicado",
            "phone": "3001111111"
        }
    )

    response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Duplicado 2",
            "phone": "3002222222"
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Está intentando crear un paciente duplicado"
    )


def test_invalid_document():

    response = client.post(
        "/patients/",
        json={
            "document": "ABC123",
            "full_name": "Paciente Test",
            "phone": "3001234567"
        }
    )

    assert response.status_code == 422


def test_invalid_phone():

    response = client.post(
        "/patients/",
        json={
            "document": "123456789",
            "full_name": "Paciente Test",
            "phone": "ABCDEF"
        }
    )

    assert response.status_code == 422