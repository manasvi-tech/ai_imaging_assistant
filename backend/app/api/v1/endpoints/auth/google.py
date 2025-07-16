from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.services.oauth import oauth
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import create_access_token
from app.core.config import settings
from app.core.constants import DEFAULT_AVATAR_URL

router = APIRouter()

@router.get("/login/google", tags=["OAuth"])
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback", tags=["OAuth"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        raise Exception("Missing user info from token")

    email = user_info["email"]
    name = user_info.get("name", "User")  # fallback in case name is missing
    picture = user_info.get("picture") or DEFAULT_AVATAR_URL.format(name=name.replace(" ", "+"))

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            id=str(uuid4()),
            email=email,
            name=name,
            profile_picture=picture,
            auth_provider="google",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
