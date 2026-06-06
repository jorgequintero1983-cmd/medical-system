from unittest.mock import patch

import pytest
import random
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


@pytest.mark.integracion
def test_get_patients():
    response = client.get("/patients/")

    assert response.status_code == 200


@pytest.mark.integracion
def test_create_patient():
    document = str(random.randint(1000000000, 9999999999))

    with patch.object(client, "post", wraps=client.post) as mock_post:
        response = client.post(
            "/patients/",
            json={
                "document": document,
                "full_name": "Paciente Integracion",
                "phone": "3001111111",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["document"] == document
        mock_post.assert_called_once()


@pytest.mark.integracion
def test_update_patient():
    document = str(random.randint(1000000000, 9999999999))

    create_response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Editar",
            "phone": "3001111111",
        },
    )

    patient_id = create_response.json()["id"]

    with patch.object(client, "put", wraps=client.put) as mock_put:
        response = client.put(
            f"/patients/{patient_id}",
            json={
                "document": document,
                "full_name": "Paciente Editado",
                "phone": "3002222222",
            },
        )

        assert response.status_code == 200
        assert response.json()["full_name"] == "Paciente Editado"
        mock_put.assert_called_once()


@pytest.mark.integracion
def test_update_patient_not_found():
    response = client.put(
        "/patients/999999",
        json={
            "document": "123456789",
            "full_name": "Paciente",
            "phone": "3001111111",
        },
    )

    assert response.status_code == 404


@pytest.mark.integracion
def test_delete_patient():
    document = str(random.randint(1000000000, 9999999999))

    create_response = client.post(
        "/patients/",
        json={
            "document": document,
            "full_name": "Paciente Eliminar",
            "phone": "3001111111",
        },
    )

    patient_id = create_response.json()["id"]

    with patch.object(client, "delete", wraps=client.delete) as mock_delete:
        response = client.delete(f"/patients/{patient_id}")

        assert response.status_code == 200
        mock_delete.assert_called_once()


@pytest.mark.integracion
def test_delete_patient_not_found():
    response = client.delete("/patients/999999")

    assert response.status_code == 404
