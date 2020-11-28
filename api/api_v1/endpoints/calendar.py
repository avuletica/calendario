import io
from http import HTTPStatus
from typing import Any

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
from schemas import ApartmentCalendarCreate

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
    obj_in = ApartmentCalendarCreate(**calendar)
    crud.apartment_calendar.create(db=db, obj_in=obj_in)


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

    output = io.BytesIO(calendar.ics_file)
    headers = {
        "Content-Disposition": f"attachment; filename=export_{calendar.id}.ics",
        "Content-Type": "text/calendar",
    }
    return StreamingResponse(output, headers=headers, media_type="text/calendar")
