from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from api import deps
from schemas.user import UserCreate

router = APIRouter()


@router.post("/registration", response_model=schemas.User)
def registration(user_in: UserCreate, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
