from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import models
from api import deps
from schemas import ApartmentCalendarCreate

router = APIRouter()


@router.post("/import", status_code=HTTPStatus.NO_CONTENT)
async def calendar_import(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    file: UploadFile = File(...),
) -> Any:
    file_ = await file.read()
    calendar = crud.apartment_calendar.parse_icalendar(file_)

    apartment = crud.apartment.get_by_name(
        db, owner_id=current_user.id, apartment_name=calendar["apartment_name"]
    )
    if not apartment:
        raise HTTPException(
            status_code=400,
            detail=f"Apartment {calendar['apartment_name']} does not exist, import failed.",
        )

    calendar["apartment_id"] = apartment.id
    apartment_calendar = crud.apartment_calendar.get_by_apartment_id(
        db, apartment_id=apartment.id
    )
    if apartment_calendar:
        raise HTTPException(
            status_code=409,
            detail="Calendar already exists for this apartment.",
        )

    calendar.pop("apartment_name", None)
    obj_in = ApartmentCalendarCreate(**calendar)
    crud.apartment_calendar.create(db=db, obj_in=obj_in)

    return Response(status_code=HTTPStatus.NO_CONTENT)
