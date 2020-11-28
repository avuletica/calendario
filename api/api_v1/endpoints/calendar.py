from datetime import datetime, date
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
from icalendar import Calendar
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
    gcal = Calendar.from_ical(file_)
    ac = {}
    for component in gcal.walk():
        if component.name == "VEVENT":
            ac["summary"] = component.get("summary")
            ac["start_datetime"] = component.get("dtstart").dt
            ac["end_datetime"] = component.get("dtend").dt
            if isinstance(ac["start_datetime"], date):
                ac["start_datetime"] = datetime.combine(
                    ac["start_datetime"], datetime.min.time()
                )
            if isinstance(ac["end_datetime"], date):
                ac["end_datetime"] = datetime.combine(
                    ac["end_datetime"], datetime.min.time()
                )

    prod_id = gcal.get("PRODID")
    apartment = crud.apartment.get_by_name(
        db, owner_id=current_user.id, apartment_name=prod_id
    )
    if not apartment:
        raise HTTPException(
            status_code=400,
            detail=f"Apartment {prod_id} does not exist, import failed.",
        )

    apartment_calendar = crud.apartment_calendar.get_by_apartment_id(db, apartment_id=apartment.id)
    if apartment_calendar:
        raise HTTPException(
            status_code=409,
            detail="Calendar already exists for this apartment.",
        )

    ac["apartment_id"] = apartment.id
    ac["ics_file"] = file_
    obj_in = ApartmentCalendarCreate(**ac)
    crud.apartment_calendar.create(db=db, obj_in=obj_in)

    return Response(status_code=HTTPStatus.NO_CONTENT)
