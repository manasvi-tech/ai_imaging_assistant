class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Medical Imaging Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    MEDICAL_UPLOADS_DIR: str = "./medical_uploads"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgre@localhost:5432/medical_db"

    # Google Cloud AI
    GCP_PROJECT: str
    DOCAI_PROCESSOR_ID: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]

    # File Storage
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")

    class Config:
        case_sensitive = True
        env_file = ".env"
 