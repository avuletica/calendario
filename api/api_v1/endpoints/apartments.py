from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps
from schemas.apartment import ApartmentCreate, Apartment

router = APIRouter()


@router.post("", response_model=schemas.Apartment)
def create_apartment(
    *,
    current_user: models.User = Depends(deps.get_current_active_user),
    apartment_in: ApartmentCreate,
    db: Session = Depends(deps.get_db)
) -> Apartment:
    apartment = crud.apartment.get_by_name(
        db, owner_id=current_user.id, apartment_name=apartment_in.name
    )
    if apartment:
        raise HTTPException(
            status_code=400,
            detail="The apartment with this name already exists in the system.",
        )
    apartment = crud.apartment.create(db, obj_in=apartment_in)
    return apartment


@router.get("", response_model=List[schemas.Apartment])
def list_apartments(
    *,
    current_user: models.User = Depends(deps.get_current_active_user),
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    apartments = crud.apartment.get_multi_by_owner(
        db=db, owner_id=current_user.id, offset=offset, limit=limit
    )
    return apartments
