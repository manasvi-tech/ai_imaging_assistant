from sqlalchemy import text
from app.db import Base, engine

# ✅ Import all models here so they are registered
from app.db.models.user import User
from app.db.models.patient import Patient
from app.db.models.scan import Scan
from app.db.models.report import Report

def initialize_database():
    """Initialize the database by creating all tables"""
    print("\n🔥 Attempting to create tables...")
    Base.metadata.create_all(bind=engine)

    # Verification
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        ))
        tables = [row[0] for row in result]
        print("\n📋 Existing tables:", tables)

if __name__ == "__main__":
    initialize_database()
