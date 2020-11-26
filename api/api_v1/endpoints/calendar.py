from typing import Any

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from icalendar import Calendar
from sqlalchemy.orm import Session

import crud
import models
from api import deps

router = APIRouter()


@router.post("/import", status_code=204)
async def calendar_import(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        file: UploadFile = File(...),
) -> Any:
    gcal = Calendar.from_ical(await file.read())
    apartment_calendar = {}
    for component in gcal.walk():
        if component.name == "VEVENT":
            apartment_calendar["summary"] = component.get("summary")
            apartment_calendar["startdt"] = component.get("dtstart").dt
            apartment_calendar["enddt"] = component.get("dtend").dt

    apartment = crud.apartment.get_by_name(
        db, owner_id=current_user.id, apartment_name=gcal.get("PRODID")
    )
    if not apartment:
        raise HTTPException(
            status_code=400,
            detail="User does not own apartment identified by `PRODID`, import failed.",
        )

    apartment_calendar["apartment_id"] = apartment.id
    apartment_calendar["ics_file"] = await file.read()
    crud.apartment_calendar.create(db, apartment_calendar)

    return None, 204
