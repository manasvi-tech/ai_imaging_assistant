
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import uuid4
from pydantic import BaseModel, EmailStr
from app.schemas.user import UserCreate
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.constants import DEFAULT_AVATAR_URL
from fastapi import Form

router = APIRouter()

class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup/email", tags=["EmailAuth"])
def signup_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=str(uuid4()),
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        profile_picture=DEFAULT_AVATAR_URL.format(name=user_data.name.replace(" ", "+")),
        role=user_data.role,
        auth_provider="local"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/email", tags=["EmailAuth"])
def login_email(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}