import io
from copy import deepcopy
from datetime import datetime
from http import HTTPStatus
from typing import Any, Optional

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Response,
    status,
)
from pydantic import AnyHttpUrl
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

import crud
import models
from api import deps
from api.utils.utils import (
    calculate_availability,
    eliminate_overlaps,
    datetime_range,
)
from schemas import ApartmentCalendarCreate, ApartmentCalendarEntryCreate

router = APIRouter()


def calendar_import_handler(db, current_user, calendar):
    apartment = crud.apartment.get_by_name(
        db, owner_id=current_user.id, apartment_name=calendar["apartment_name"]
    )
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apartment {calendar['apartment_name']} does not exist, import failed.",
        )

    calendar["apartment_id"] = apartment.id
    apartment_calendar = crud.apartment_calendar.get_by_apartment_id(
        db, apartment_id=apartment.id
    )
    if apartment_calendar:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Calendar already exists for this apartment.",
        )

    calendar.pop("apartment_name", None)
    entries = calendar.pop("entries")
    apartment_calendar_in = ApartmentCalendarCreate(**calendar)
    apartment_calendar = crud.apartment_calendar.create(
        db=db, obj_in=apartment_calendar_in
    )

    for entry in entries:
        entry["apartment_calendar_id"] = apartment_calendar.id
        apartment_calendar_entry_in = ApartmentCalendarEntryCreate(**entry)
        crud.apartment_calendar_entry.create(db=db, obj_in=apartment_calendar_entry_in)


@router.post("/import", status_code=HTTPStatus.NO_CONTENT)
async def calendar_import(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    file: UploadFile = File(...),
) -> Any:
    file_ = await file.read()
    calendar = crud.apartment_calendar.parse_icalendar(file_)
    calendar_import_handler(db, current_user, calendar)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.get(
    "/import-from-url",
    responses={
        204: {
            "description": "Import complete.",
        },
        400: {
            "description": "Apartment does not exist.",
        },
        409: {
            "description": "Calendar already exists for this apartment.",
        },
    },
)
async def calendar_import_from_url(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    url: AnyHttpUrl,
) -> Any:
    calendar_from_url = await crud.apartment_calendar.fetch_icalendar_from_url(url)
    calendar = crud.apartment_calendar.parse_icalendar(calendar_from_url)
    calendar["import_url"] = url
    calendar_import_handler(db, current_user, calendar)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.get(
    "/export/{calendar_id}",
    responses={
        200: {
            "description": "Returns file.",
        },
        403: {
            "description": "Forbidden",
        },
        404: {
            "description": "Calendar does not exist.",
        },
    },
)
async def calendar_export(
    calendar_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    calendar = crud.apartment_calendar.get_by_id(db, calendar_id)

    if not calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar does not exist.",
        )

    if calendar.apartment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    output = io.BytesIO(calendar.file)
    headers = {
        "Content-Disposition": f"attachment; filename=export_{calendar.id}.ics",
        "Content-Type": "text/calendar",
    }
    return StreamingResponse(output, headers=headers, media_type="text/calendar")


@router.get("")
def list_apartment_calendars(
    datetime_from: datetime,
    datetime_to: datetime,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Cleaning time is scheduled from 11:00 AM to 15:00 PM

    Algorithm flow:

       --------------|-------------|-------------|
    A1 [date_range_1, date_range_2, date_range_3]
       --------------|-------------|
    A2 [date_range_1, date_range_2]
       --------------|-------------|-------------|
    A3 [date_range_1, date_range_2, date_range_3]
       --------------|-------------|-------------|-------------|
    A4 [date_range_1, date_range_2, date_range_3, date_range_4]

    For given datetime range

    1) Find intervals when the apartment is unoccupied
        - This is done by combining apartment first end_datetime (end of stay) with apartments
        next start_time (next guest coming) and generating datetime range
    2) If there is a booking on the same day guest leaves that day will be optimal cleaning time.
    3) If we find common intervals where apartments are unoccupied => result in group cleaning
        - this is done by checking if there is an intersection in the available days of each apartment.
            a) If there is an intersection => find availability_range with the most number of intersections,
                this will result in most apartment cleaning per day.
            b) All availability_ranges that fall under the previous category will be removed for the next iteration
            c) Repeat process as long as there are common intervals.
    4) If there is no common interval where apartments are unoccupied suggest the first available cleaning and that is:
        - same day if the guest leaves at or before 11 AM
        - next day if the guest leaves after 3 PM
    """

    apartments = crud.apartment.get_multi_by_owner(db=db, owner_id=current_user.id)

    if not apartments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not own any apartments.",
        )

    calendar_ids = [
        apartment.calendar.id
        for apartment in apartments
        if apartment.calendar is not None
    ]

    calendar_entries = crud.apartment_calendar_entry.get_multi_by_calendar_id(
        db,
        apartment_calendar_ids=calendar_ids,
        datetime_from=datetime_from,
        datetime_to=datetime_to,
    )

    apartment_entries = {str(apartment.id): [] for apartment in apartments}
    for entry in calendar_entries:
        data = {
            "start_datetime": entry.start_datetime,
            "end_datetime": entry.end_datetime,
        }
        apartment_entries[str(entry.calendar.apartment_id)].append(data)

    cleaning_schedule = {
        apartment.name: {
            "entries": apartment_entries[str(apartment.id)],
            "next_cleaning_time": None,
            "availability_range": [],
        }
        for apartment in apartments
    }

    for item in cleaning_schedule.values():
        availability_ranges, next_cleaning_time = calculate_availability(
            item["entries"]
        )
        item["next_cleaning_time"] = next_cleaning_time
        item["availability_range"].extend(availability_ranges)
        del item["entries"]

    while any(item.get("availability_range") for item in cleaning_schedule.values()):
        remaining_availability = []
        for key, value in cleaning_schedule.items():
            availability_range = value.get("availability_range")

            if availability_range is None or len(availability_range) == 0:
                continue

            remaining_availability.append(
                {
                    "apartment_name": key,
                    "availability_range": availability_range[0],
                }
            )

        elimination = eliminate_overlaps(*remaining_availability)
        for apartment in elimination["apartments"]:
            cleaning_schedule[apartment]["next_cleaning_time"].append(
                elimination["next_cleaning_time"]
            )
            cleaning_schedule[apartment]["availability_range"].pop()

            if len(cleaning_schedule[apartment]["availability_range"]) == 0:
                del cleaning_schedule[apartment]["availability_range"]

    for item in cleaning_schedule.values():
        item["next_cleaning_time"].sort()

    return cleaning_schedule
