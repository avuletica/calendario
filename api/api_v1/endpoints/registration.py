from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import schemas
from api import deps
from models.user import User
from schemas.user import UserCreate, User

router = APIRouter()


@router.post("/registration", response_model=schemas.User)
def registration(user_in: UserCreate, db: Session = Depends(deps.get_db)) -> User:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    return user
