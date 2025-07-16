# backend/app/api/v1/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

# Re-export the get_db dependency for endpoints
get_db_dependency = Depends(get_db)