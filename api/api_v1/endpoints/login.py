from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from api import deps
from config import settings
from core import security

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    payload: schemas.LoginPayload,
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud.user.authenticate(db, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
