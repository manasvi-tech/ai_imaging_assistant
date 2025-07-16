from app.db.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@123gmail.com").first()
        if admin:
            # Update existing admin if needed
            admin.role = "admin"
            admin.hashed_password = pwd_context.hash("adminRocks")
            print("Admin user updated")
        else:
            # Create new admin
            admin = User(
                email="admin@123gmail.com",
                name="Admin",
                profile_picture="",
                role="admin",
                hashed_password=pwd_context.hash("adminRocks")
            )
            db.add(admin)
            print("Admin user created")
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()