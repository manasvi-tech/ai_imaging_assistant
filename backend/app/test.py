from app.db.session import SessionLocal
from app.db.models.scan import Scan

def fix_invalid_scans():
    db = SessionLocal()
    try:
        # Find scans with no patient_id
        invalid_scans = db.query(Scan).filter(Scan.patient_id == None).all()
        
        if not invalid_scans:
            print("No invalid scans found")
            return
        
        print(f"Found {len(invalid_scans)} invalid scans")
        
        # Either delete them or assign to patient 1 (example)
        for scan in invalid_scans:
            scan.patient_id = 1  # Assign to your existing patient
            # OR: db.delete(scan)
        
        db.commit()
        print("Fixed invalid scans")
    finally:
        db.close()

if __name__ == "__main__":
    fix_invalid_scans()