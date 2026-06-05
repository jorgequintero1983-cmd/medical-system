from fastapi.testclient import TestClient
from backend.app.main import app
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
            "full_name": "Paciente Integracion",
            "phone": "3001111111"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document"] == document


def test_update_patient():

    document = str(random.randint(100000000, 999999999))

    create_response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Editar",
            "phone": "3001111111"
        }
    )

    patient_id = create_response.json()["id"]

    response = client.put(
        f"/patients/{patient_id}",
        json={
            "document": document,
            "full_name": "Paciente Editado",
            "phone": "3002222222"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Paciente Editado"


def test_update_patient_not_found():

    response = client.put(
        "/patients/999999",
        json={
            "document": "123456789",
            "full_name": "Paciente",
            "phone": "3001111111"
        }
    )

    assert response.status_code == 404


def test_delete_patient():

    document = str(random.randint(100000000, 999999999))

    create_response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Eliminar",
            "phone": "3001111111"
        }
    )

    patient_id = create_response.json()["id"]

    response = client.delete(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 200


def test_delete_patient_not_found():

    response = client.delete(
        "/patients/999999"
    )

    assert response.status_code == 404