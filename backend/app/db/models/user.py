from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class UserRole(str, enum.Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # nullable for OAuth-only users
    role = Column(Enum(UserRole), default=UserRole.student)
    auth_provider = Column(String, default="local")  # or "google", "github"
    reports = relationship("Report", back_populates="author")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
