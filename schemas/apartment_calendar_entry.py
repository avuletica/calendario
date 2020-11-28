from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ApartmentCalendarEntryBase(BaseModel):
    summary: Optional[str]
    start_datetime: datetime
    end_datetime: datetime
    apartment_calendar_id: int

    class Config:
        arbitrary_types_allowed = True


# Properties to receive via API on creation
class ApartmentCalendarEntryCreate(ApartmentCalendarEntryBase):
    pass


class ApartmentCalendarEntryInDB(ApartmentCalendarEntryBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ApartmentCalendarEntry(ApartmentCalendarEntryInDB):
    pass
