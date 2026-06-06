from unittest.mock import patch

import pytest


@pytest.mark.integracion
@patch(
    "backend.app.api.routes.auth_routes.jwt.encode",
    return_value="mock-token-integracion",
)
def test_login_success(mock_jwt_encode, client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "mock-token-integracion"
    mock_jwt_encode.assert_called_once()


@pytest.mark.integracion
@patch(
    "backend.app.api.routes.auth_routes.verify_password",
    return_value=False,
)
def test_login_invalid_password(mock_verify_password, client):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "xxxx",
        },
    )

    assert response.status_code == 401
    mock_verify_password.assert_called_once()


@pytest.mark.integracion
def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "noexiste@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 401
