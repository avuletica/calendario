from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


# Shared properties
class ApartmentCalendarBase(BaseModel):
    import_url: Optional[AnyHttpUrl]

    class Config:
        arbitrary_types_allowed = True


# Properties to receive via API on creation
class ApartmentCalendarCreate(ApartmentCalendarBase):
    file: bytes
    apartment_id: int


class ApartmentCalendarInDB(ApartmentCalendarBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class ApartmentCalendar(ApartmentCalendarInDB):
    pass
