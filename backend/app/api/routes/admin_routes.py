from fastapi import APIRouter, Depends

from backend.app.core.security import require_admin

router = APIRouter()


# =========================
# ADMIN ONLY
# =========================

@router.get("/admin/dashboard")
def admin_dashboard(
    current_user = Depends(require_admin)
):

    return {
        "message": "Welcome admin",
        "user": current_user.username
    }