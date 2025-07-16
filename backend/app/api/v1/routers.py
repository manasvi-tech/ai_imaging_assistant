from fastapi import APIRouter
from app.api.v1.endpoints import patients, scans, auth, admin, reports



api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")  # ✅ Let nested routers define their own tags
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(scans.router, prefix="/scans", tags=["Scans"])
api_router.include_router(admin.router, prefix="/auth", tags=["Admin"])
api_router.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
