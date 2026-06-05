from sqlalchemy.orm import Session

from backend.app.models.user_model import User

from backend.app.schemas.user_schema import UserCreate

from backend.app.core.security import hash_password, verify_password


# =========================
# CREATE USER
# =========================

def create_user(
    db: Session,
    user: UserCreate
):

    hashed = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        role=user.role
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


# =========================
# AUTHENTICATE USER
# =========================

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user