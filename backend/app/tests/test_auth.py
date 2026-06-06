import pytest
from fastapi.testclient import TestClient

from backend.app.api.routes import auth_routes
from backend.app.main import app
from backend.app.tests.mocks.db_mock import (
    ADMIN_PASSWORD_HASH,
    build_mock_db,
    build_mock_user,
    override_get_db,
)

client = TestClient(app)


@pytest.mark.unitaria
def test_login_success():
    mock_db = build_mock_db()
    mock_db.query.return_value.filter.return_value.first.return_value = (
        build_mock_user()
    )
    app.dependency_overrides[auth_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@test.com",
                "password": "123456",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    mock_db.query.assert_called()


@pytest.mark.unitaria
def test_login_wrong_password():
    mock_db = build_mock_db()
    mock_db.query.return_value.filter.return_value.first.return_value = (
        build_mock_user(hashed_password=ADMIN_PASSWORD_HASH)
    )
    app.dependency_overrides[auth_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@test.com",
                "password": "incorrecta",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401


@pytest.mark.unitaria
def test_login_user_not_found():
    mock_db = build_mock_db()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[auth_routes.get_db] = override_get_db(mock_db)

    try:
        response = client.post(
            "/auth/login",
            json={
                "email": "noexiste@test.com",
                "password": "123456",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
