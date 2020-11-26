from datetime import datetime
from typing import Optional, BinaryIO

from pydantic import BaseModel


# Shared properties
class ApartmentCalendarBase(BaseModel):
    summary: str
    start_datetime: datetime
    end_datetime: datetime
    ics_file: BinaryIO
    apartment_id: int

    class Config:
        arbitrary_types_allowed = True


# Properties to receive via API on creation
class ApartmentCalendarCreate(ApartmentCalendarBase):
    pass


class ApartmentCalendarInDB(ApartmentCalendarBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ApartmentCalendar(ApartmentCalendarInDB):
    pass
