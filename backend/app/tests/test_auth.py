from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "incorrecta"
        }
    )

    assert response.status_code == 401


def test_login_user_not_found():

    response = client.post(
        "/auth/login",
        json={
            "email": "noexiste@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401