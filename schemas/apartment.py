from typing import Optional

from pydantic import BaseModel


# Shared properties
class ApartmentBase(BaseModel):
    name: str
    owner_id: int


# Properties to receive via API on creation
class ApartmentCreate(ApartmentBase):
    pass


class ApartmentInDB(ApartmentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Apartment(ApartmentInDB):
    pass
