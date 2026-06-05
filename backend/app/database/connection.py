from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =========================
# URL DE POSTGRES
# =========================

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/medical_db"

# =========================
# ENGINE
# =========================

engine = create_engine(DATABASE_URL)

# =========================
# SESSION
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE
# =========================

Base = declarative_base()