from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================
# IMPORTAR RUTAS
# =========================

from backend.app.api.routes.auth_routes import router as auth_router
from backend.app.api.routes.patient_routes import router as patient_router
from backend.app.api.routes.admin_routes import router as admin_router

# =========================
# CREAR APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REGISTRAR RUTAS
# =========================

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(admin_router)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "API funcionando correctamente"
    }