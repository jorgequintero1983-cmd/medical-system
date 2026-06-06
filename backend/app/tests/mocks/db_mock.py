"""Helpers para mocks de SQLAlchemy en pruebas unitarias."""

from unittest.mock import MagicMock

from backend.app.models.user_model import User

ADMIN_PASSWORD_HASH = (
    "$2b$12$AsnHg/.BJ6ESCtyolKS3FOf9/k9.Y2M.vr66ISvLVxJBlWIp4RihO"
)


def build_mock_user(
    email="admin@test.com",
    username="admin",
    hashed_password=ADMIN_PASSWORD_HASH,
    role="admin",
):
    user = MagicMock(spec=User)
    user.email = email
    user.username = username
    user.hashed_password = hashed_password
    user.role = role
    return user


def build_mock_db():
    mock_db = MagicMock()
    query = MagicMock()
    mock_db.query.return_value = query
    query.filter.return_value.first.return_value = None
    query.all.return_value = []
    return mock_db


def override_get_db(mock_db):
    def _get_db():
        yield mock_db

    return _get_db
