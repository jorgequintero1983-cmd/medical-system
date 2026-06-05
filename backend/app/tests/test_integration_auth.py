def test_login_success(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "xxxx"
        }
    )

    assert response.status_code == 401


def test_login_user_not_found(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "noexiste@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401