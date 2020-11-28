import io
from typing import Any

from fastapi import (
    APIRouter,
)
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get(
    "/calendar/export",
    responses={
        200: {
            "description": "Returns file.",
        }
    },
)
async def calendar_export() -> Any:
    """
    Test calendar import from URL.
    """
    ics = """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:apartment_2
        CALSCALE:GREGORIAN
        METHOD:PUBLISH
        BEGIN:VEVENT
        DTSTART;VALUE=DATE:20200930
        DTEND;VALUE=DATE:20201003
        UID:631670f42e602f90050dc56fa57c59c6
        SUMMARY: Perica
        END:VEVENT
        BEGIN:VEVENT
        DTSTART;VALUE=DATE:20201005
        DTEND;VALUE=DATE:20201010
        UID:c536ad531e27361c80cf28e9f355bdef
        SUMMARY:Ante
        END:VEVENT
        END:VCALENDAR
    """.replace(
        " ", ""
    )
    output = io.StringIO(ics)
    headers = {
        "Content-Disposition": f"attachment; filename=export.ics",
        "Content-Type": "text/calendar",
    }
    return StreamingResponse(output, headers=headers, media_type="text/calendar")
