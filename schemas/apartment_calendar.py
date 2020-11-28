from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


# Shared properties
class ApartmentCalendarBase(BaseModel):
    summary: str
    start_datetime: datetime
    end_datetime: datetime
    ics_file: bytes
    apartment_id: int
    import_url: Optional[AnyHttpUrl]

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
