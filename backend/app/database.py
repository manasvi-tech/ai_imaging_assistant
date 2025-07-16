# backend/app/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
from .base import Base
from .models import Patient  # Now safe to import

# Configure logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgre@localhost:5432/medical_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("\n🔥 Attempting to create tables...")
    Base.metadata.create_all(bind=engine)
    
    # Verification
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row.table_name for row in result]
        print("\n📋 Existing tables:", tables)
        
        if 'patients' not in tables:
            print("❌ Patients table missing - creating directly...")
            Patient.__table__.create(engine)
            print("✅ Patients table created")

if __name__ == "__main__":
    init_db()