from fastapi import APIRouter
from .google import router as google_router
from .email import router as email_router
from .profile import router as profile_router

router = APIRouter()
router.include_router(google_router)  # Don't add prefix or tag here
router.include_router(email_router)   # Don't add prefix or tag here
router.include_router(profile_router, tags=["Profile"])