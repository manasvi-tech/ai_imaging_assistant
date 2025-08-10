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
        # Re-fetch user from the active session
        db_user = db.query(User).filter(User.id == current_user.id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update only provided fields
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.profile_picture is not None:
            db_user.profile_picture = user_data.profile_picture
        if user_data.email is not None:
            db_user.email = user_data.email

        db_user.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
