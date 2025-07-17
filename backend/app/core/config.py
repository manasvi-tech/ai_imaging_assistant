from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Better path handling
HF_TOKEN = os.getenv("HF_TOKEN")

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Medical Imaging Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Media and File Storage Settings
    MEDIA_ROOT: str = os.path.join(BASE_DIR, "media")  # Base media directory
    MEDICAL_UPLOADS_DIR: str = os.path.join(MEDIA_ROOT, "medical_uploads")  # For original uploads
    SEGMENTATION_OUTPUT_DIR: str = os.path.join(MEDIA_ROOT, "segmentations")  # For segmentation results
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")  # For static files
    
    # Authentication
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    HF_TOKEN: str
    GEMINI_API_KEY: str # Gemini API key
    FRONTEND_URL: str = "http://localhost:5173" 

    # Database
    DATABASE_URL: str
    
    # External Services
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")  # Hugging Face API key
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"
        
settings = Settings()