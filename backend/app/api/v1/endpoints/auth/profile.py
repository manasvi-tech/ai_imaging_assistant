from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.user import UserOut, UserUpdate
from datetime import datetime
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.user import UserOut, UserUpdate
from datetime import datetime
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Update only the fields that are provided
        if user_data.name is not None:
            current_user.name = user_data.name
        if user_data.profile_picture is not None:
            current_user.profile_picture = user_data.profile_picture
        
        current_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@router.get("/last-login")
def get_last_login(current_user: User = Depends(get_current_user)):
    return {"last_login": current_user.last_login}