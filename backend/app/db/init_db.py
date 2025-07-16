# backend/app/db/init_db.py
from sqlalchemy import text
from app.db import Base, engine

def initialize_database():
    """Initialize the database by creating all tables"""
    print("\n🔥 Attempting to create tables...")
    Base.metadata.create_all(bind=engine)
    
    # Verification
    with engine.connect() as conn:
        # Remove the incorrect next() call and use text() properly
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row[0] for row in result]
        print("\n📋 Existing tables:", tables)
        
        if 'patients' not in tables:
            print("❌ Patients table missing - creating directly...")
            from app.db.models.patient import Patient
            Patient.__table__.create(engine)
            print("✅ Patients table created")

if __name__ == "__main__":
    initialize_database()