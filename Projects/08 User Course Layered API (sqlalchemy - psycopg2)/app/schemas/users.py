from datetime import datetime

from db.models.user import RoleEnum
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum


class UserCreate(UserBase): ...


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    role: RoleEnum | None = None
    is_active: bool | None = None
