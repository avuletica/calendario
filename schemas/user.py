from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = "John Doe"


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr = "john@doe.com"
    password: str = "password"


class UserInDBBase(UserBase):
    id: Optional[int] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
