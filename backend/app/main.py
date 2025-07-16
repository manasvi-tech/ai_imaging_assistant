# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

from app.api.v1.routers import api_router
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings

from fastapi.security import OAuth2PasswordBearer
auth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/email")


def create_tables():
    """Create database tables on startup"""
    Base.metadata.create_all(bind=engine)

def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 🔐 Add this line (SessionMiddleware)
    app.add_middleware(SessionMiddleware, secret_key="session-key")

    # Static files
    app.mount(
        "/static",
        StaticFiles(directory=settings.STATIC_DIR),
        name="static"
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    def on_startup():
        create_tables()

    return app


app = get_application()