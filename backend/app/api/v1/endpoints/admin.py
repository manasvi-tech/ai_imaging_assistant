# app/api/v1/endpoints/admin.py

from fastapi import APIRouter, Depends
from app.db.models.user import User, UserRole
from app.core.security import require_roles

router = APIRouter()

@router.get("/admin")
def get_admin_dashboard(current_user: User = Depends(require_roles([UserRole.admin]))):
    return {"message": f"Welcome, {current_user.name}!"}
